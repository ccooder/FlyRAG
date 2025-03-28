#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:19
import asyncio
import json
from ctypes.wintypes import HTASK
from typing import List, Union

from sqlmodel import SQLModel, Field

from common.redis_client import RedisClient
from flyrag.api.entity import Document, DocumentChunk
from flyrag.task import DocumentTaskStatus, TaskPipeline, REDIS_KEY_PIPELINE_FLAG, REDIS_KEY_PIPELINE_QUEUE, \
    chunking_pipeline, embedding_pipeline
from flyrag.task.chunking_pipeline import ChunkingPipeline
from flyrag.task.embedding_pipeline import EmbeddingPipeline


def chunking_pipeline_in_process():
    asyncio.run(ChunkingPipeline().start())


class TaskDispatcher(object):
    __instance = None
    __is_first = True
    __redis = RedisClient().get_redis()

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if TaskDispatcher.__is_first:
            TaskDispatcher.__is_first = False

    @classmethod
    async def start_pipeline(cls):
        await cls.__redis.set(REDIS_KEY_PIPELINE_FLAG, 1)
        from multiprocessing import Process
        # 启动切片进程
        chunking = Process(target=chunking_pipeline_in_process, name='p-chunking')
        chunking.start()
        embedding = Process(target=EmbeddingPipeline().start, name='p-embedding')
        embedding.start()

    @classmethod
    async def stop_pipeline(cls):
        await cls.__redis.set(REDIS_KEY_PIPELINE_FLAG, 0)

    @classmethod
    async def dispatch_task(cls, tasks: List[Union[Document, DocumentChunk]], status: DocumentTaskStatus):
        tasks_dump = [task.model_dump_json() for task in tasks]
        if status == DocumentTaskStatus.CHUNKING:
            await cls.__redis.lpush(REDIS_KEY_PIPELINE_QUEUE.format(chunking_pipeline.name), *tasks_dump)
        elif status == DocumentTaskStatus.CHUNKED:
            await cls.__redis.lpush(REDIS_KEY_PIPELINE_QUEUE.format(embedding_pipeline.name), *tasks_dump)
