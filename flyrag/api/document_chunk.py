#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/17 20:19
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import func
from sqlmodel import Session, select, col

from common.mysql_client import MysqlClient
from flyrag.api import R, Page
from flyrag.api.entity import DocumentChunkQuery, DocumentChunk
from flyrag.api.service.document_chunk_service import DocumentChunkService

router = APIRouter(prefix='/chunk', tags=["document_chunk"])

SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]

@router.post("/list")
async def list_chunk(chunk_query: DocumentChunkQuery, session: SessionDep, current: int = 1,
                   size: Annotated[int, Query(le=100)] = 10):
    if not chunk_query.doc_id:
        return R.fail('文档id不能为空')
    # 查询列表
    offset, limit = (current - 1) * size, size
    docs = DocumentChunkService.list_chunk(chunk_query, session, offset, limit)
    # 查询总数
    count_statement = MysqlClient.fill_statement(select(func.count(col(DocumentChunk.id))), DocumentChunk, chunk_query)
    count_statement = count_statement.where(DocumentChunk.doc_id == chunk_query.doc_id)
    total = session.exec(count_statement).one()

    page = Page.of(current=current, size=size, total=total, records=docs)
    return R.ok(data=page)

@router.post("/toggle")
async def toggle(id: int, session: SessionDep):
    if not id:
        return R.fail('id不能为空')
    chunk = session.get(DocumentChunk, id)
    if not chunk:
        return R.fail('段落不存在')
    if chunk.status == 1:
        result = await DocumentChunkService.disable_chunk(chunk, session)
    else:
        result = await DocumentChunkService.enable_chunk(chunk, session)
    return R.handle(result)