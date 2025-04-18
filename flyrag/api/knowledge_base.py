#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 11:07
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy import update, func
from sqlmodel import Session, select, col

import common
from flyrag.api import R, Page
from flyrag.api.entity import KnowledgeBase, KnowledgeBaseUpdate, DeleteEntity, KnowledgeBaseQuery, KnowledgeBaseCreate, \
    Document, KnowledgeBaseRecall
from common.mysql_client import MysqlClient
from flyrag.api.service.document_service import DocumentService

router = APIRouter(prefix='/kb', tags=["knowledge_base"])
SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]


@router.post("/create")
async def create_kb(kb_create: KnowledgeBaseCreate, session: SessionDep):
    if not kb_create.name:
        return R.fail('知识库名称不能为空')
    if not kb_create.chunk_config:
        return R.fail('知识库配置不能为空')
    try:
        session.add(kb_create.get_kb())
        # 若存在切片配置，保存
        chunk_config = kb_create.chunk_config
        if chunk_config:
            chunk_config.target_id = kb_create.get_kb().id
            session.add(chunk_config)
        # 若存在检索配置，保存
        retrival_config = kb_create.retrival_config
        if retrival_config:
            retrival_config.kb_id = kb_create.get_kb().id
            session.add(retrival_config)
        if kb_create.docs and len(kb_create.docs) > 0:
            DocumentService.create_docs(kb_create.id, kb_create.docs, session)
        session.commit()
    except Exception as e:
        common.get_logger().error("创建知识库报错:{}", e)
        session.rollback()
        return R.fail('创建失败')
    return R.ok('创建成功')


@router.get("/fetch")
async def fetch_kb(id: int, session: SessionDep):
    kb = session.get(KnowledgeBase, id)
    return R.ok(data=kb)


@router.post("/update")
async def update_kb(kb: KnowledgeBaseUpdate, session: SessionDep):
    if not kb.id:
        return R.fail('id不能为空')
    kb_db = session.get(KnowledgeBase, kb.id)
    if not kb_db:
        return R.fail('知识库不存在')
    kb_data = kb.model_dump(exclude_unset=True)
    kb_db.sqlmodel_update(kb_data)
    session.add(kb_db)
    session.commit()
    return R.ok('更新成功')


@router.post("/delete")
async def delete_kb(kb: DeleteEntity, session: SessionDep):
    if not kb.id:
        return R.fail('id不能为空')
    kb_db = session.get(KnowledgeBase, kb.id)
    if not kb_db:
        return R.fail('知识库不存在')
    kb_db.sqlmodel_update(kb)
    session.add(kb_db)
    # 删除知识库下的所有文档
    session.exec(update(Document).where(Document.kb_id == kb.id).values(is_deleted=1))
    session.commit()
    return R.ok('删除成功')


@router.post("/list")
async def list_kb(kb: KnowledgeBaseQuery, session: SessionDep, current: int = 1,
                  size: Annotated[int, Query(le=100)] = 100):
    # 查询列表
    offset, limit = (current - 1) * size, size
    statement = MysqlClient.fill_statement(select(KnowledgeBase).offset(offset).limit(limit), KnowledgeBase, kb)
    # 如果有自定义查询字段，请在此自行添加
    kbs = session.exec(statement).all()

    # 查询总数
    count_statement = MysqlClient.fill_statement(select(func.count(col(KnowledgeBase.id))), KnowledgeBase, kb)
    total = session.exec(count_statement).one()

    page = Page.of(current=current, size=size, total=total, records=kbs)
    return R.ok(data=page)

@router.post("/recall")
async def recall(kb_recall: KnowledgeBaseRecall, session: SessionDep):
    kb = session.get(KnowledgeBase, kb_recall.kb_id)
    if not kb:
        return R.fail('知识库不存在')
    from flyrag.module.retrival.rag_fusion_retriever import RagFusionRetriever
    result = RagFusionRetriever(kb_recall.kb_id, kb_recall.query).retrieve(kb_recall.retrival_config)
    return R.ok(data=result)
