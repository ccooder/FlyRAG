#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/3 11:38
from sqlmodel import Session, select

from flyrag.api.entity import Model


class ModelService(object):
    @staticmethod
    def get_model(model_id: int, session: Session) -> Model:
        model = session.exec(select(Model).where(Model.id == model_id)).one()
        return model