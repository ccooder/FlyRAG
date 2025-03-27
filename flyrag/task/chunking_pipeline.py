#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import json
import time

from redis.asyncio import Redis

import common
from common.minio_client import MinioClient
from common.mysql_client import MysqlClient
from common.redis_client import RedisClient
from flyrag.api.entity import Entity, Document
from flyrag.api.service.chunk_config_service import ChunkConfigService
from flyrag.module.chunk import ChunkerContext, ChunkMode
from flyrag.module.document import DocumentParserContext
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT, PIPELINE_LIMIT, REDIS_KEY_PIPELINE_QUEUE, \
    REDIS_KEY_PIPELINE_FLAG

name = 'chunking'


class ChunkingPipeline(TaskPipeline):
    __redis: Redis = RedisClient().get_redis()

    async def start(self):
        while int((await self.__redis.get(REDIS_KEY_PIPELINE_FLAG)).decode('utf-8')):
            # 判断流水线执行任务数是否达到限制
            task_count = await self.__redis.get(REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
            if task_count is None:
                task_count = 0
                await self.__redis.set(REDIS_KEY_PIPELINE_TASK_COUNT.format(name), task_count)
            else:
                task_count = int(task_count.decode('utf-8'))
            if task_count >= PIPELINE_LIMIT:
                time.sleep(1)
                continue

            # Lua 脚本
            script = """
                    local doc = redis.call('RPOP', KEYS[1])
                    if doc then
                        redis.call('INCR', KEYS[2])
                    end
                    return doc
                    """

            # 执行 Lua 脚本
            doc = await self.__redis.eval(script, 2, REDIS_KEY_PIPELINE_QUEUE.format(name),
                                          REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
            if doc is None:
                time.sleep(1)
                continue
            # 判断任务是否暂停
            if await super().is_pause(doc, name):
                continue

            # 执行任务
            await self.execute(doc)

            # 休眠1秒
            time.sleep(1)

    async def execute(self, doc: str):
        # TODO NFL 切片的逻辑
        doc = Document(**json.loads(doc))
        # 初始化文档处理进度
        await super().incr_progress(doc.id, 0)
        file_path = MinioClient().get_presigned_url(common.DEFAULT_BUCKET_NAME, doc.obj_name)
        content = DocumentParserContext.do_parse(file_path)
        # 解析完文档，进度增加0.05
        await super().incr_progress(doc.id, 0.05)
        # 获取文档的切片配置
        chunk_config = ChunkConfigService().get_chunk_config(doc.chunk_config_id, next(MysqlClient().get_session()))
        # 不同的切片模式，返回的切片数据结构不一样
        if chunk_config.mode == ChunkMode.General:
            chunks = ChunkerContext.do_chunk(content, doc, chunk_config)
            # 保存切片到数据库

        # 切片入库后进度增加0.05
        await super().incr_progress(doc.id, 0.05)
        pass
