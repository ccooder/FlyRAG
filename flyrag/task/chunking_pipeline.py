#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import time

from redis.asyncio import Redis

from common.redis_client import RedisClient
from flyrag.api.entity import Entity, Document
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT, PIPELINE_LIMIT, REDIS_KEY_PIPELINE_QUEUE, \
    REDIS_KEY_PIPELINE_FLAG

name = 'chunking'


class ChunkingPipeline(TaskPipeline):
    __redis: Redis = RedisClient().get_redis()
    flag = True

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

            # 执行任务
            self.execute(doc)

            # 休眠1秒
            time.sleep(1)

    def execute(self, doc: Document):
        # TODO NFL 切片的逻辑
        print('切片逻辑', doc)
        pass
