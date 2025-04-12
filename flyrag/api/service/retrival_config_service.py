#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/12 15:41
from sqlmodel import Session, select

from flyrag.api.entity import RetrivalConfig


class RetrivalConfigService(object):
    @staticmethod
    def get_retrival_config(kb_id: int, session: Session) -> RetrivalConfig:
        chunk_config = session.exec(select(RetrivalConfig).where(RetrivalConfig.kb_id == kb_id)).one()
        return chunk_config