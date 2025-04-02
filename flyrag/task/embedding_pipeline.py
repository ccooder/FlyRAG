#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import json
import time

from common.weaviate_client import WeaviateClient
from flyrag.api.entity import DocumentChunk
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT, \
    REDIS_KEY_PIPELINE_QUEUE

name = 'embedding'


class EmbeddingPipeline(TaskPipeline):
    async def start(self):
        while await super().pipeline_flag():
            if await super().is_over_limit(name):
                continue
            # Lua 脚本
            script = """
                    local chunk = redis.call('RPOP', KEYS[1])
                    if chunk then
                        redis.call('INCR', KEYS[2])
                    end
                    return chunk
                    """

            # 执行 Lua 脚本
            chunk_redis = await self._redis.eval(script, 2, REDIS_KEY_PIPELINE_QUEUE.format(name),
                                                 REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
            if chunk_redis is None:
                time.sleep(1)
                continue
            chunk = DocumentChunk(**json.loads(chunk_redis))
            # 判断任务是否暂停
            if await super().is_pause(chunk.doc_id, name):
                # 若任务暂停放回队列底部并且将执行中的数量-1
                pipeline = self._redis.pipeline()
                pipeline.multi()
                await pipeline.lpush(REDIS_KEY_PIPELINE_QUEUE.format(name), chunk_redis)
                await pipeline.decr(REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
                await pipeline.execute()
                continue
            # 执行任务
            await self.execute(chunk)

            # 休眠1秒
            time.sleep(1)

    async def execute(self, chunk: DocumentChunk):
        with WeaviateClient().get_client() as weaviate_client:
            WeaviateVec

        pass
