#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/19 21:05
import asyncio
from copy import deepcopy
from typing import List, Type

from sqlmodel import Session, select

from common import snowflake
from common.mysql_client import MysqlClient
from common.snowflake import Snowflake
from flyrag.api.entity import Document, DocumentUpdate, ChunkConfig, DocumentQuery
from flyrag.api.enums import ChunkConfigType
from flyrag.task import DocumentTaskStatus



class DocumentService(object):

    @staticmethod
    def create_docs(kb_id: int, docs: List[Document], session: Session):
        cc = session.exec(select(ChunkConfig).where(ChunkConfig.target_id == kb_id)).one()
        doc_ccs = []
        for doc in docs:
            doc.kb_id = kb_id
            doc.chunk_mode = cc.mode
            doc_cc = ChunkConfig(**cc.model_dump(exclude=['id', 'create_time', 'update_time']))
            doc_cc.type = ChunkConfigType.DOCUMENT.value
            doc_cc.target_id = doc.id
            doc_ccs.append(doc_cc)
        deepcopy_docs = deepcopy(docs)
        from flyrag.task.task_dispatcher import TaskDispatcher
        asyncio.create_task(TaskDispatcher.dispatch_task(deepcopy_docs, DocumentTaskStatus.CHUNKING))
        session.add_all(docs)
        session.add_all(doc_ccs)




    @staticmethod
    def get_doc(doc_id: int, session: Session) -> Type[Document]:
        return session.get(Document, doc_id)

    @staticmethod
    def list_doc(doc_query: DocumentQuery, session: Session, offset: int=0, limit: int=1000) -> List[Document]:
        statement = MysqlClient.fill_statement(select(Document).offset(offset).limit(limit), Document, doc_query)
        # 如果有自定义查询字段，请在此自行添加
        if doc_query.kb_id:
            statement = statement.where(Document.kb_id == doc_query.kb_id)
        docs = session.exec(statement).all()
        return docs

    @staticmethod
    def update_doc(doc: DocumentUpdate, session: Session, autocommit: bool = True):
        if not doc.id:
            return False
        doc_in_db = session.get(Document, doc.id)
        if not doc_in_db:
            return False
        doc_data = doc.model_dump(exclude_unset=True)
        doc_in_db.sqlmodel_update(doc_data)
        session.add(doc_in_db)
        if autocommit:
            session.commit()
        return True
