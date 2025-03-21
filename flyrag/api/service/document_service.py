#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/19 21:05
import asyncio
from copy import deepcopy
from typing import List, Type

from sqlmodel import Session, select

from common import snowflake
from common.snowflake import Snowflake
from flyrag.api.entity import Document, DocumentUpdate, ChunkConfig
from flyrag.task import DocumentTaskStatus
from flyrag.task.task_dispatcher import TaskDispatcher


class DocumentService(object):

    @staticmethod
    def create_docs(kb_id: int, docs: List[Document], session: Session):
        cc = session.exec(select(ChunkConfig).where(ChunkConfig.target_id == kb_id)).one()
        doc_ccs = []
        for doc in docs:
            doc.kb_id = kb_id
            doc.chunk_mode = cc.mode
            doc_cc = ChunkConfig(**cc.model_dump(exclude=['id']))
            doc_cc.target_id = doc.id
            doc_ccs.append(doc_cc)
        deepcopy_docs = deepcopy(docs)
        asyncio.create_task(TaskDispatcher.dispatch_document(deepcopy_docs, DocumentTaskStatus.CHUNKING))
        session.add_all(docs)
        session.add_all(doc_ccs)




    @staticmethod
    def get_doc(doc_id: int, session: Session) -> Type[Document]:
        return session.get(Document, doc_id)

    @staticmethod
    def update_doc(doc: DocumentUpdate, session: Session):
        if not doc.id:
            return False
        doc_in_db = session.get(Document, doc.id)
        if not doc_in_db:
            return False
        doc_data = doc.model_dump(exclude_unset=True)
        doc_in_db.sqlmodel_update(doc_data)
        session.add(doc_in_db)
        session.commit()
        return True
