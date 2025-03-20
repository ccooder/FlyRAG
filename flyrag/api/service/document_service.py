#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/19 21:05
import asyncio
from copy import deepcopy
from typing import List, Type

from sqlmodel import Session

from flyrag.api.entity import Document
from flyrag.task import DocumentTaskStatus
from flyrag.task.task_dispatcher import TaskDispatcher


class DocumentService(object):

    @staticmethod
    def create_docs(kb_id: int, docs: List[Document], session: Session):

        for doc in docs:
            doc.kb_id = kb_id
        deepcopy_docs = deepcopy(docs)
        asyncio.create_task(TaskDispatcher.dispatch_document(deepcopy_docs, DocumentTaskStatus.CHUNKING))
        session.add_all(docs)

    @staticmethod
    def get_doc(doc_id: int, session: Session) -> Type[Document]:
        return session.get(Document, doc_id)
