#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 17:28
from typing import List, Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session

from flyrag.api import R
from flyrag.api.entity import Document
from common.mysql_client import MysqlClient

router = APIRouter(prefix='/document', tags=["document"])

SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]


@router.post("/create")
async def create_doc(docs: List[Document], session: SessionDep):
    if len(docs) == 0:
        return R.fail('文档数量不能为0')
    session.add_all(docs)
    session.commit()
    return R.success('文档添加成功')
