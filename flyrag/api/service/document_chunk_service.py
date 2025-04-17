#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/28 10:15
import asyncio
from copy import deepcopy
from typing import List

from sqlalchemy import delete
from sqlmodel import Session, select

from common.mysql_client import MysqlClient
from flyrag.api.entity import DocumentChunk, DocumentChunkQuery
from flyrag.task import DocumentTaskStatus


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
