#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/28 10:15
import asyncio
from copy import deepcopy
from typing import List, Type

from sqlalchemy import delete
from sqlmodel import Session, select

import common
from common.mysql_client import MysqlClient
from common.redis_client import RedisClient
from flyrag.api.entity import DocumentChunk, DocumentChunkQuery, DocumentChunkVidQuery
from flyrag.api.service.document_chunk_vid_service import DocumentChunkVidService
from flyrag.task import DocumentTaskStatus, REDIS_KEY_PIPELINE_QUEUE, embedding_pipeline


class DocumentChunkService(object):
    @staticmethod
    def create_chunks(chunks: List[DocumentChunk], session: Session):
        chunks_copy = deepcopy(chunks)
        session.add_all(chunks)
        from flyrag.task.task_dispatcher import TaskDispatcher
        asyncio.create_task(TaskDispatcher.dispatch_task(chunks_copy, DocumentTaskStatus.CHUNKED))

    @staticmethod
    def delete_chunks(chunk_query: DocumentChunkQuery, session: Session, autocommit: bool = True):
        statement = MysqlClient.fill_statement(delete(DocumentChunk), DocumentChunk, chunk_query)
        # 如果有自定义查询字段，请在此自行添加
        if chunk_query.doc_id:
            statement = statement.where(DocumentChunk.doc_id == chunk_query.doc_id)
        if chunk_query.chunk_id:
            statement = statement.where(DocumentChunk.chunk_id == chunk_query.chunk_id)
        result = session.exec(statement)

        if autocommit:
            session.commit()
        return result.rowcount

    @staticmethod
    def list_chunk(chunk_query: DocumentChunkQuery, session: Session, offset: int = 0, limit: int = 10):
        statement = MysqlClient.fill_statement(select(DocumentChunk)
                                               .offset(offset)
                                               .limit(limit), DocumentChunk, chunk_query)
        # 如果有自定义查询字段，请在此自行添加
        if chunk_query.doc_id:
            statement = statement.where(DocumentChunk.doc_id == chunk_query.doc_id)
        chunks = session.exec(statement).all()
        return chunks

    @staticmethod
    def get_chunks(chunk_ids: List[int], session: Session):
        statement = select(DocumentChunk).where(DocumentChunk.id.in_(chunk_ids))
        return session.exec(statement).all()

    @staticmethod
    async def disable_chunk(chunk: Type[DocumentChunk], session: Session):
        try:
            # 删除向量关联
            await DocumentChunkVidService.delete_vids(DocumentChunkVidQuery(chunk_id=chunk.id), session, autocommit=False)
            chunk_update = DocumentChunk(id=chunk.id, status=0)
            chunk.sqlmodel_update(chunk_update.model_dump(exclude_unset=True))
            session.add(chunk)
            session.commit()
            return True
        except Exception as e:
            common.get_logger().error('禁用切片[id={}]报错:{}', chunk.id, e)
            session.rollback()
        return False

    @staticmethod
    async def enable_chunk(chunk: Type[DocumentChunk], session: Session):
        try:
            chunk_copy = deepcopy(chunk)
            chunk_update = DocumentChunk(id=chunk.id, status=1)
            chunk.sqlmodel_update(chunk_update.model_dump(exclude_unset=True))
            session.add(chunk)
            # 将启用的段落加个塞儿，立即执行
            await RedisClient().get_aredis().rpush(REDIS_KEY_PIPELINE_QUEUE.format(embedding_pipeline.name),
                                                   chunk_copy.model_dump_json())
            session.commit()
            return True
        except Exception as e:
            common.get_logger().error('启用切片[id={}]报错:{}', chunk.id, e)
            session.rollback()
        return False
