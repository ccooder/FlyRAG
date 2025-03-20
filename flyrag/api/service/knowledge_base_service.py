#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/20 15:11
from sqlalchemy import func
from sqlmodel import Session, select, col

from flyrag.api.entity import KnowledgeBase


class KnowledgeBaseService(object):
    @staticmethod
    def exists(kb_id: int, session: Session):
        kb = session.exec(select(func.count(col(KnowledgeBase.id))).where(KnowledgeBase.id == kb_id)).one()
        return kb > 0
