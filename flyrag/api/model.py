#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/20 11:50
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import load_only
from sqlmodel import Session, select, col

import common
from common.mysql_client import MysqlClient
from flyrag.api import R, Page
from flyrag.api.entity import Model, ModelQuery

router = APIRouter(prefix='/model', tags=["model"])
SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]


@router.post("/list")
async def list_model(mq: ModelQuery, session: SessionDep, current: int = 1,
                     size: Annotated[int, Query(le=100)] = 100):
    # 查询列表
    offset, limit = (current - 1) * size, size
    statement = MysqlClient.fill_statement(select(Model).options(load_only(Model.id, Model.name)).offset(offset).limit(limit), Model, mq)
    # 如果有自定义查询字段，请在此自行添加
    statement = statement.where(Model.type == mq.type)
    models = session.exec(statement).all()

    # 查询总数
    count_statement = MysqlClient.fill_statement(select(func.count(col(Model.id))), Model, mq)
    count_statement = count_statement.where(Model.type == mq.type)
    total = session.exec(count_statement).one()
    page = Page.of(current=current, size=size, total=total, records=models)
    return R.ok(data=page)
