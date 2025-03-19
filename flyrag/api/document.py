#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 17:28
import asyncio
from copy import deepcopy
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.sql.coercions import expect
from sqlmodel import Session, select, col

from flyrag.api import R
from flyrag.api.entity import DocumentCreate, KnowledgeBase
from common.mysql_client import MysqlClient
from flyrag.api.service.document_service import DocumentService
from flyrag.task import DocumentTaskStatus
from flyrag.task.task_dispatcher import TaskDispatcher

router = APIRouter(prefix='/document', tags=["document"])

SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]


@router.post("/create")
async def create_doc(doc_create: DocumentCreate, session: SessionDep):

    try:
        if len(doc_create.docs) == 0:
            return R.fail('文档数量不能为0')
        if not doc_create.kb_id:
            return R.fail('知识库id不能为空')
        kb = session.exec(select(func.count(col(KnowledgeBase.id))).where(KnowledgeBase.id == doc_create.kb_id)).one()
        if kb == 0:
            return R.fail('知识库不存在')

        DocumentService.create_docs(session, doc_create.kb_id, doc_create.docs)
        deepcopy_docs = deepcopy(doc_create.docs)
        session.commit()
    except Exception as e:
        session.rollback()
    asyncio.create_task(TaskDispatcher.dispatch_document(deepcopy_docs, DocumentTaskStatus.CHUNKING))

    return R.ok('文档添加成功')