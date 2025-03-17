#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:19
from typing import List

from flyrag.api.entity import Document
from flyrag.task import DocumentTaskStatus, TaskPipeline
from flyrag.task.chunking_pipeline import ChunkingPipeline
from flyrag.task.embedding_pipeline import EmbeddingPipeline


class TaskDispatcher(object):
    __instance = None
    __is_first = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if TaskDispatcher.__is_first:
            TaskDispatcher.__is_first = False

    @staticmethod
    def start_pipeline():
        from multiprocessing import Process
        # 启动切片进程
        chunking = Process(target=ChunkingPipeline().start, name='p-chunking')
        chunking.start()
        embedding = Process(target=EmbeddingPipeline().start, name='p-embedding')
        embedding.start()

    def dispatch_document(self, docs: List[Document], status: DocumentTaskStatus):
        pass
