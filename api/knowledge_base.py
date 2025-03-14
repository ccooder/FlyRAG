#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 11:07
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlmodel import Session, select

from api import R
from api.entity import KnowledgeBase, KnowledgeBaseUpdate, DeleteEntity, KnowledgeBaseQuery
from common.mysql_client import MysqlClient

router = APIRouter(prefix='/kb', tags=["knowledge_base"])
SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]
@router.post("/create")
async def create_kb(kb: KnowledgeBase, session: SessionDep):
    session.add(kb)
    session.commit()
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
async def delete_kb(kb : DeleteEntity, session: SessionDep):
    if not kb.id:
        return R.fail('id不能为空')
    kb_db = session.get(KnowledgeBase, kb.id)
    if not kb_db:
        return R.fail('知识库不存在')
    kb_db.sqlmodel_update(kb)
    session.add(kb_db)
    session.commit()
    return R.ok('删除成功')

@router.post("/list")
async def list_kb(kb: KnowledgeBaseQuery, session: SessionDep, offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100):
    statement = MysqlClient.fill_statement(select(KnowledgeBase).offset(offset).limit(limit), KnowledgeBase, kb)
    # 如果有自定义查询字段，请在此自行添加
    kbs = session.exec(statement).all()
    return R.ok(data=kbs)