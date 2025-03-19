#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/19 21:05
from copy import deepcopy
from typing import List

from sqlmodel import Session

from flyrag.api.entity import Document


class DocumentService(object):
    @staticmethod
    def create_docs(session: Session, kb_id: int, docs: List[Document]):
        for doc in docs:
            doc.kb_id = kb_id
        print("123123123", docs)
        session.add_all(docs)
