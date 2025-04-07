#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/7 17:15
from typing import List

from sqlmodel import Session

from flyrag.api.entity import DocumentContent


class DocumentContentService(object):
    @staticmethod
    def create_content(content: DocumentContent, session: Session):
        session.add(content)
        session.commit()