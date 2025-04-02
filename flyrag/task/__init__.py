#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:00
import json
import time
from abc import ABC, abstractmethod
from enum import Enum, auto

from redis import Redis

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
    _redis: Redis = RedisClient().get_redis()

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    def execute(self, task: str):
        pass

    async def pipeline_flag(self):
        return int((await self._redis.get(REDIS_KEY_PIPELINE_FLAG)).decode('utf-8'))

    async def is_over_limit(self, pipeline_name):
        # 判断流水线执行任务数是否达到限制
        task_count = await self._redis.get(REDIS_KEY_PIPELINE_TASK_COUNT.format(pipeline_name))
        if task_count is None:
            task_count = 0
            await self._redis.set(REDIS_KEY_PIPELINE_TASK_COUNT.format(pipeline_name), task_count)
        else:
            task_count = int(task_count.decode('utf-8'))
        if task_count >= PIPELINE_LIMIT:
            time.sleep(1)
            return True
        return False

    async def is_pause(self, doc_id: int, pipeline_name):
        session = next(MysqlClient().get_session())
        doc_db = session.get(Document, doc_id)
        if doc_db.pause == 1:
            return True
        return False

    async def change_status(self, doc: Document, pipeline_name: str, status: DocumentStatus):
        session = next(MysqlClient().get_session())
        try:
            doc_db = session.get(Document, doc.id)
            doc_data = Document(status=status.value).model_dump(exclude_unset=True)
            doc_db.sqlmodel_update(doc_data)
            session.add(doc_db)
            if status == DocumentStatus.AVAILABLE:
                # TODO NFL 索引完成时的操作
                pass
            session.commit()
        except Exception as e:
            common.get_logger().error('更新文档状态时报错{}', e)
            session.rollback()
            # 若任务状态更改失败放回队列底部并且将执行中的数量-1
            pipeline = self._redis.pipeline()
            pipeline.multi()
            await pipeline.lpush(REDIS_KEY_PIPELINE_QUEUE.format(pipeline_name), doc.model_dump_json())
            await pipeline.decr(REDIS_KEY_PIPELINE_TASK_COUNT.format(pipeline_name))
            await pipeline.execute()
            return False
        return True

    async def incr_progress(self, doc_id: int, progress: float):
        if not await self._redis.exists(REDIS_KEY_DOC_PROGRESS.format(doc_id)):
            await self._redis.set(REDIS_KEY_DOC_PROGRESS.format(doc_id), progress)
        else:
            await self._redis.incrbyfloat(REDIS_KEY_DOC_PROGRESS.format(doc_id), progress)



class DocumentTaskStatus(Enum):
    """
    此状态只适用于文档上传后的处理流程中与数据库所存的文档状态有所区别
    """
    QUEUEING = auto(),
    CHUNKING = auto(),
    CHUNKED = auto(),
    INDEXING = auto(),
    INDEXED = auto(),
