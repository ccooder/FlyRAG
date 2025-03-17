#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import time

import common
from common.redis_client import RedisClient
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT

name = 'chunking'

class ChunkingPipeline(TaskPipeline):

    def __init__(self):
        super().__init__()

    def start(self):
        redis = RedisClient().get_redis()
        while True:
            # 判断流水线执行任务数是否达到限制
            common.get_logger().info(f'{name} pipeline task count: {redis.get(REDIS_KEY_PIPELINE_TASK_COUNT.format(name))}')
            time.sleep(1)
            # 获取任务
            # redis.rpop()
        pass