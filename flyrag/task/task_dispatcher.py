#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:19
import asyncio
import json
from typing import List

from sqlmodel import SQLModel, Field

from common.redis_client import RedisClient
from flyrag.api.entity import Document
from flyrag.task import DocumentTaskStatus, TaskPipeline, REDIS_KEY_PIPELINE_FLAG, REDIS_KEY_PIPELINE_QUEUE, \
    chunking_pipeline
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
    async def dispatch_document(cls, docs: List[Document], status: DocumentTaskStatus):
        docs_dump = [doc.model_dump_json() for doc in docs]
        if status == DocumentTaskStatus.CHUNKING:
            await cls.__redis.lpush(REDIS_KEY_PIPELINE_QUEUE.format(chunking_pipeline.name), *docs_dump)
        pass

class Test(SQLModel):
    id:int = Field(default=None)
    name:str = Field(default=None)
    docs:List[Document] = Field(default=None)

if __name__ == '__main__':
    t = Test(id=1, name='niufenglu', docs=[
        {
            "name": "仲裁须知.pdf",
            "original_name": "仲裁须知.pdf",
            "size": 133026,
            "obj_name": "fly-rag/ae8a84e2-0492-11f0-b5e6-d651885abef6.pdf"
        }
    ])
    print(t.docs[0].model_dump())