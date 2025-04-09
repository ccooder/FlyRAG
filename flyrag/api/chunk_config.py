#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/20 10:48
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlmodel import Session, select

import common
from common.mysql_client import MysqlClient
from flyrag.api import R
from flyrag.api.entity import ChunkConfig
from flyrag.api.enums import ChunkConfigType
from flyrag.api.service.document_service import DocumentService
from flyrag.api.service.knowledge_base_service import KnowledgeBaseService

router = APIRouter(prefix='/chunk_config', tags=["chunk_config"])
SessionDep = Annotated[Session, Depends(MysqlClient().get_session)]


@router.post("/submit")
async def submit_cc(cc: ChunkConfig, session: SessionDep):
    try:
        if cc.chunk_size > 2048:
            return R.fail('切片大小不能超过2048')
        if cc.chunk_size < 1:
            return R.fail('切片大小不能小于1')
        if cc.chunk_overlap > cc.chunk_size:
            return R.fail('切片重叠不能超过切片大小')
        if cc.type == ChunkConfigType.KNOWLEDGE_BASE.value:
            kb = KnowledgeBaseService.exists(cc.target_id, session)
            if not kb:
                return R.fail('知识库不存在')
        elif cc.type == ChunkConfigType.DOCUMENT.value:
            doc = DocumentService.get_doc(cc.target_id, session)
            if not doc:
                return R.fail('文档不存在')
            # # 查询是否存在知识库级的配置，如没有，使用文档的配置 实际场景中知识库的配置是最先设置的
            # config = session.exec(
            #     select(func.count(col(ChunkConfig.id))).where(ChunkConfig.target_id == doc.kb_id)).one()
            # if config == 0:
            #     cc_kb = deepcopy(cc)
            #     cc_kb.target_id = doc.kb_id
            #     session.add(cc_kb)

        # 若已存在该配置，则更新
        cc_in_db = session.exec(select(ChunkConfig).where(ChunkConfig.target_id == cc.target_id)).all()
        if len(cc_in_db) > 1:
            common.get_logger().error('{}[target_id={}]存在多个切片配置，请检查', ChunkConfigType(cc.type).name, cc.target_id)
            session.rollback()
            return R.fail('切片配置错误')
        elif len(cc_in_db) == 1:
            kb_data = cc.model_dump(exclude_unset=True)
            cc_in_db[0].sqlmodel_update(kb_data)
            session.add(cc_in_db[0])
        else:
            session.add(cc)
        session.commit()
    except Exception as e:
        common.get_logger().error('保存切片配置时报错{}', e)
        session.rollback()
        return R.fail('配置失败')

    return R.ok('配置成功')

@router.get("/fetch")
async def fetch_cc(target_id: int, session: SessionDep):
    cc = session.exec(select(ChunkConfig).where(ChunkConfig.target_id == target_id)).one()
    return R.ok(data=cc)
