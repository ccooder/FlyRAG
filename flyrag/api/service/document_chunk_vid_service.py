#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/7 17:09
from typing import List

from sqlmodel import Session

from flyrag.api.entity import DocumentChunkVid


class DocumentChunkVidService(object):
    @staticmethod
    def create_chunk_vid(chunk_vids: List[DocumentChunkVid], session: Session):
        session.add_all(chunk_vids)
        session.commit()
