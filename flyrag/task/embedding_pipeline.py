#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import time

import common
from flyrag.api.entity import Entity, Document
from flyrag.task import TaskPipeline

name = 'embedding'


class EmbeddingPipeline(TaskPipeline):

    def start(self):
        while True:
            common.get_logger().info(456)
            time.sleep(2)

    def execute(self, doc: Document):
        pass
