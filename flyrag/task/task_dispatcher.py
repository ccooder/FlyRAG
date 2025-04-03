#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:19
import asyncio
import json
import time
from ctypes.wintypes import HTASK
from typing import List, Union

from sqlmodel import SQLModel, Field

import common
from common.mysql_client import MysqlClient
from common.redis_client import RedisClient
from flyrag.api.entity import Document, DocumentChunk, DocumentUpdate
from flyrag.api.enums import DocumentStatus
from flyrag.api.service.document_service import DocumentService
from flyrag.task import DocumentTaskStatus, TaskPipeline, REDIS_KEY_PIPELINE_FLAG, REDIS_KEY_PIPELINE_QUEUE, \
    chunking_pipeline, embedding_pipeline
from flyrag.task.chunking_pipeline import ChunkingPipeline
from flyrag.task.embedding_pipeline import EmbeddingPipeline


def chunking_pipeline_in_subprocess():
    asyncio.run(ChunkingPipeline().start())

def embedding_pipeline_in_subprocess():
    asyncio.run(EmbeddingPipeline().start())


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
        for i in range(4):
            chunking = Process(target=chunking_pipeline_in_subprocess, name=f'p-chunking-{i}')
            chunking.start()
            embedding = Process(target=embedding_pipeline_in_subprocess, name=f'p-embedding-{i}')
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
        elif status == DocumentTaskStatus.INDEXED:
            session = next(MysqlClient().get_session())
            try:
                for doc in tasks:
                    DocumentService.update_doc(DocumentUpdate(id=doc.id, status=DocumentStatus.AVAILABLE), session, False)
            except Exception as e:
                session.rollback()
                common.get_logger().error('更新文档为可用状态时报错{}', e)
                return
            session.commit()

