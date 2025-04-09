#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/9 16:54
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session, select

import common
from common.mysql_client import MysqlClient
from flyrag.api import R
from flyrag.api.entity import RetrivalConfig
from flyrag.api.service.knowledge_base_service import KnowledgeBaseService

router = APIRouter(prefix='/retrival_config', tags=["retrival_config"])
SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]


@router.post("/submit")
async def submit_rc(rc: RetrivalConfig, session: SessionDep):
    try:
        if not rc.kb_id:
            return R.fail('知识库ID不能为空')

        kb = KnowledgeBaseService.exists(rc.kb_id, session)
        if not kb:
                return R.fail('知识库不存在')


        # 若已存在该配置，则更新
        rc_in_db = session.exec(select(RetrivalConfig).where(RetrivalConfig.kb_id == rc.kb_id)).all()
        if len(rc_in_db) > 1:
            common.get_logger().error('知识库[kb_id={}]存在多个检索配置，请检查', rc.target_id)
            session.rollback()
            return R.fail('配置失败')
        elif len(rc_in_db) == 1:
            rc_data = rc.model_dump(exclude_unset=True)
            rc_in_db[0].sqlmodel_update(rc_data)
            session.add(rc_in_db[0])
        else:
            session.add(rc)
        session.commit()
    except Exception as e:
        common.get_logger().error('保存检索配置时报错{}', e)
        session.rollback()
        return R.fail('配置失败')

    return R.ok('配置成功')

@router.get("/fetch")
async def fetch_rc(kb_id: int, session: SessionDep):
    rc = session.exec(select(RetrivalConfig).where(RetrivalConfig.kb_id == kb_id)).one()
    return R.ok(data=rc)
