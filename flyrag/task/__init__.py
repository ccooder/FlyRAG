#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:00
import json
from abc import ABC, abstractmethod
from enum import Enum, auto

import common
from common.mysql_client import MysqlClient
from common.redis_client import RedisClient
from flyrag.api.entity import Entity, Document
from flyrag.api.enums import DocumentStatus

name = 'task'

PIPELINE_LIMIT = 4
REDIS_KEY_PIPELINE_FLAG = 'flyrag:pipeline_flag'
REDIS_KEY_PIPELINE_TASK_COUNT = 'flyrag:pipeline_task_count:{}'
REDIS_KEY_PIPELINE_QUEUE = 'flyrag:pipeline_queue:{}'
REDIS_KEY_DOC_PROGRESS = 'flyrag:doc_progress:{}'


class TaskPipeline(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def execute(self, task: str):
        pass

    async def is_pause(self, task: str, pipeline_name):
        session = next(MysqlClient().get_session())
        redis = RedisClient().get_redis()
        doc = Document(**json.loads(task))
        doc_db = session.get(Document, doc.id)
        if doc_db.pause == 1:
            print("任务暂停暂时放回队列底部")
            # 若任务暂停放回队列底部并且将执行中的数量-1
            pipeline = redis.pipeline()
            pipeline.multi()
            await pipeline.lpush(REDIS_KEY_PIPELINE_QUEUE.format(pipeline_name), task)
            await pipeline.decr(REDIS_KEY_PIPELINE_TASK_COUNT.format(pipeline_name))
            await pipeline.execute()
            return True
        return False

    async def change_status(self, doc: Document, pipeline_name: str, status: DocumentStatus):
        session = next(MysqlClient().get_session())
        redis = RedisClient().get_redis()
        try:
            doc_data = Document(status=status.value).model_dump(exclude_unset=True)
            doc.sqlmodel_update(doc_data)
            session.add(doc)
            if status == DocumentStatus.AVAILABLE:
                # TODO NFL 索引完成时的操作
                pass
            session.commit()
        except Exception as e:
            common.get_logger().error('更新文档状态时报错{}', e)
            session.rollback()
            # 若任务状态更改失败放回队列底部并且将执行中的数量-1
            pipeline = redis.pipeline()
            pipeline.multi()
            await pipeline.lpush(REDIS_KEY_PIPELINE_QUEUE.format(pipeline_name), doc.model_dump_json())
            await pipeline.decr(REDIS_KEY_PIPELINE_TASK_COUNT.format(pipeline_name))
            await pipeline.execute()
            return False
        return True

    async def incr_progress(self, doc_id: int, progress: float):
        redis = RedisClient().get_redis()
        if await redis.exists(REDIS_KEY_DOC_PROGRESS.format(doc_id)):
            await redis.set(REDIS_KEY_DOC_PROGRESS.format(doc_id), progress)
        else:
            await redis.incrby(REDIS_KEY_DOC_PROGRESS.format(doc_id), progress)



class DocumentTaskStatus(Enum):
    """
    此状态只适用于文档上传后的处理流程中与数据库所存的文档状态有所区别
    """
    QUEUEING = auto(),
    CHUNKING = auto(),
    CHUNKED = auto(),
    INDEXING = auto(),
    INDEXED = auto(),
