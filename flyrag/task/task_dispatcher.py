#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:19
import asyncio
from typing import List, Union

from langchain_weaviate import WeaviateVectorStore

import common
from common.mysql_client import MysqlClient
from common.redis_client import RedisClient
from common.weaviate_client import WeaviateClient
from flyrag.api.entity import Document, DocumentChunk, DocumentUpdate, DocumentQuery, DocumentChunkVidQuery, \
    DocumentChunkQuery
from flyrag.api.enums import DocumentStatus
from flyrag.api.service.document_chunk_service import DocumentChunkService
from flyrag.api.service.document_chunk_vid_service import DocumentChunkVidService
from flyrag.api.service.document_service import DocumentService
from flyrag.task import DocumentTaskStatus, TaskPipeline, REDIS_KEY_PIPELINE_FLAG, REDIS_KEY_PIPELINE_QUEUE, \
    chunking_pipeline, embedding_pipeline, REDIS_KEY_PIPELINE_TASK_COUNT, REDIS_KEY_DOC_PROGRESS, \
    REDIS_KEY_DOC_EMBEDDING_PROGRESS
from flyrag.task.chunking_pipeline import ChunkingPipeline
from flyrag.task.embedding_pipeline import EmbeddingPipeline


def chunking_pipeline_in_subprocess():
    asyncio.run(ChunkingPipeline().start())

def embedding_pipeline_in_subprocess():
    asyncio.run(EmbeddingPipeline().start())


class TaskDispatcher(object):
    __instance = None
    __is_first = True
    __redis = RedisClient().get_aredis()

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if TaskDispatcher.__is_first:
            TaskDispatcher.__is_first = False

    @classmethod
    async def reset_pipeline(cls):
        # 获取数据库进行中的任务
        session = next(MysqlClient().get_session())
        docs = DocumentService.list_doc(DocumentQuery(status=DocumentStatus.INDEXING.value), session)
        if len(docs) == 0:
            return
        for doc in docs:
            session = next(MysqlClient().get_session())
            doc_id = doc.id
            # TODO NFL 1. 删除切片及切片向量 2. 删除redis中的任务 3. 将文档改为排队中
            doc_vids = DocumentChunkVidService.list_vids(DocumentChunkVidQuery(doc_id=doc_id), session)
            # 遍历删除向量数据库的关联向量
            with WeaviateClient().get_client() as weaviate_client:
                wvs = WeaviateVectorStore(client=weaviate_client, index_name=common.DEFAULT_WEAVIATE_COLLECTION, text_key='text')
                ids = []
                for doc_vid in doc_vids:
                    ids.extend(doc_vid.vids.split(','))
                if len(ids) > 0:
                    await wvs.adelete(ids)
            # 删除chunk_vid
            DocumentChunkVidService.delete_vids(DocumentChunkVidQuery(doc_id=doc_id), session)
            # 删除文档切片
            DocumentChunkService.delete_chunks(DocumentChunkQuery(doc_id=doc_id), session)
            session.commit()
            # 更新文档状态为排队中
            DocumentService.update_doc(DocumentUpdate(id=doc_id, status=DocumentStatus.QUEUEING), session)
        # 清空redis任务队列与标记
        rc = RedisClient()
        await rc.delete_keys_with_prefix(REDIS_KEY_PIPELINE_TASK_COUNT.format(''))
        await rc.delete_keys_with_prefix(REDIS_KEY_PIPELINE_QUEUE.format(''))
        await rc.delete_keys_with_prefix(REDIS_KEY_DOC_PROGRESS.format(''))
        await rc.delete_keys_with_prefix(REDIS_KEY_DOC_EMBEDDING_PROGRESS.format(''))

        # 将文档重新放入待切片任务队列
        await cls.dispatch_task(docs, DocumentTaskStatus.CHUNKING)


    @classmethod
    async def start_pipeline(cls):
        # 开始流水线前，先重置进行的中的任务
        await cls.reset_pipeline()
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

