#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/28 10:15
import asyncio
from copy import deepcopy
from typing import List

from sqlmodel import Session

from flyrag.api.entity import DocumentChunk
from flyrag.task import DocumentTaskStatus



class DocumentChunkService(object):
    @staticmethod
    def create_chunks(chunks: List[DocumentChunk], session: Session):
        chunks_copy = deepcopy(chunks)
        session.add_all(chunks)
        from flyrag.task.task_dispatcher import TaskDispatcher
        asyncio.create_task(TaskDispatcher.dispatch_task(chunks_copy, DocumentTaskStatus.CHUNKED))
