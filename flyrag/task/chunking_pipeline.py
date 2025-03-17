#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import time

import common
from common.redis_client import RedisClient
from flyrag.api.entity import Entity, Document
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT, PIPELINE_LIMIT, REDIS_KEY_PIPELINE_QUEUE

name = 'chunking'


class ChunkingPipeline(TaskPipeline):


    def __init__(self):
        super().__init__()
        self.__redis = RedisClient().get_redis()

    def start(self):
        redis = RedisClient().get_redis()
        while True:
            # 判断流水线执行任务数是否达到限制
            if self.__redis.get(REDIS_KEY_PIPELINE_TASK_COUNT.format(name)) >= PIPELINE_LIMIT:
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
            doc = redis.eval(script, 2, REDIS_KEY_PIPELINE_QUEUE.format(name),
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
        pass
