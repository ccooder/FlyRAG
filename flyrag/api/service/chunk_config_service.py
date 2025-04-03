#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/27 16:22
from sqlmodel import Session, select

from flyrag.api.entity import ChunkConfig


class ChunkConfigService(object):
    @staticmethod
    def get_chunk_config(target_id: int, session: Session) -> ChunkConfig:
        chunk_config = session.exec(select(ChunkConfig).where(ChunkConfig.target_id == target_id)).one()
        return chunk_config