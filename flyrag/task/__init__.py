#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:00
from abc import ABC, abstractmethod
from enum import Enum, auto

from flyrag.api.entity import Entity

name = 'task'

PIPELINE_LIMIT = 4
REDIS_KEY_PIPELINE_FLAG = 'flyrag:pipeline_flag'
REDIS_KEY_PIPELINE_TASK_COUNT = 'flyrag:pipeline_task_count:{}'
REDIS_KEY_PIPELINE_QUEUE = 'flyrag:pipeline_queue:{}'


class TaskPipeline(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def execute(self, task: Entity):
        pass


class DocumentTaskStatus(Enum):
    """
    此状态只适用于文档上传后的处理流程中与数据库所存的文档状态有所区别
    """
    QUEUEING = auto(),
    CHUNKING = auto(),
    CHUNKED = auto(),
    INDEXING = auto(),
    INDEXED = auto(),
