#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 17:28
import asyncio
from copy import deepcopy
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import func
from sqlmodel import Session, select, col

import common
from common.minio_client import MinioClient
from flyrag.api import R, Page
from flyrag.api.entity import DocumentCreate, KnowledgeBase, DocumentQuery, Document, DocumentUpdate, DeleteEntity
from common.mysql_client import MysqlClient
from flyrag.api.enums import DocumentStatus
from flyrag.api.service.document_service import DocumentService

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
        DocumentService.create_docs(doc_create.kb_id, doc_create.docs, session)
        session.commit()
    except Exception as e:
        common.get_logger().error('创建文档时报错{}', e)
        session.rollback()

    return R.ok('文档添加成功')


@router.post("/update")
async def update_doc(doc: DocumentUpdate, session: SessionDep):
    if not doc.id:
        return R.fail('id不能为空')
    doc_in_db = session.get(Document, doc.id)
    if not doc_in_db:
        return R.fail('文档不存在')
    if doc.status:
        if doc.status != DocumentStatus.DISABLED.value and doc.status != DocumentStatus.AVAILABLE.value:
            return R.fail('只可禁用启用')
        if doc_in_db.status != DocumentStatus.DISABLED.value and doc_in_db.status != DocumentStatus.AVAILABLE.value:
            return R.fail('文档正在索引，不可更改')
        if doc.status == DocumentStatus.AVAILABLE.value and doc_in_db.status != DocumentStatus.DISABLED.value:
            return R.fail('文档未禁用，不可启用')
        if doc.status == DocumentStatus.DISABLED.value and doc_in_db.status != DocumentStatus.AVAILABLE.value:
            return R.fail('文档未启用，不可禁用')
    doc_data = doc.model_dump(exclude_unset=True)
    doc_in_db.sqlmodel_update(doc_data)
    session.add(doc_in_db)
    session.commit()
    return R.ok('更新成功')


@router.post("/delete")
async def delete_doc(doc: DeleteEntity, session: SessionDep):
    if not doc.id:
        return R.fail('id不能为空')
    doc_db = session.get(Document, doc.id)
    if not doc_db:
        return R.fail('文档不存在')
    doc_db.sqlmodel_update(doc)
    session.add(doc_db)
    if MinioClient().delete_file(common.DEFAULT_BUCKET_NAME, doc_db.obj_name):
        session.commit()
        return R.ok('删除成功')
    else:
        session.rollback()
        return R.ok('删除失败')


@router.post("/pause")
async def pause(id: int, session: SessionDep):
    doc_db = session.get(Document, id)
    if not doc_db:
        return R.fail('文档不存在')
    if doc_db.pause == 1:
        return R.fail('不可重复暂停')
    if doc_db.status != DocumentStatus.QUEUEING.value and doc_db.status != DocumentStatus.INDEXING.value:
        return R.fail('文档未在处理中，不可暂停')
    if doc_db.pause == 0:
        doc = Document(id=doc_db.id, pause=1)
        doc_db.sqlmodel_update(doc.model_dump(exclude_unset=True))
        session.add(doc_db)
        session.commit()
        return R.ok('暂停成功')


@router.post("/resume")
async def resume(id: int, session: SessionDep):
    doc_db = session.get(Document, id)
    if not doc_db:
        return R.fail('文档不存在')
    if doc_db.pause == 0:
        return R.fail('文档未暂停')
    if doc_db.pause == 1:
        doc = Document(id=doc_db.id, pause=0)
        doc_db.sqlmodel_update(doc.model_dump(exclude_unset=True))
        session.add(doc_db)
        session.commit()
        return R.ok('恢复成功')


@router.post("/list")
async def list_doc(doc_query: DocumentQuery, session: SessionDep, current: int = 1,
                   size: Annotated[int, Query(le=100)] = 100):
    # 查询列表
    offset, limit = (current - 1) * size, size
    statement = MysqlClient.fill_statement(select(Document).offset(offset).limit(limit), Document, doc_query)
    # 如果有自定义查询字段，请在此自行添加
    statement = statement.where(Document.kb_id == doc_query.kb_id)
    docs = session.exec(statement).all()

    # 查询总数
    count_statement = MysqlClient.fill_statement(select(func.count(col(Document.id))), Document, doc_query)
    count_statement = count_statement.where(Document.kb_id == doc_query.kb_id)
    total = session.exec(count_statement).one()

    page = Page.of(current=current, size=size, total=total, records=docs)
    return R.ok(data=page)
