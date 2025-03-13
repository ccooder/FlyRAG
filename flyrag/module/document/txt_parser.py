#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 20:44
from fengluU import exec_time

from flyrag.module.document import BaseParser
from langchain_community.document_loaders import TextLoader
from langchain_community.storage import


class TxtParser(BaseParser):
    @exec_time
    def parse(self):
        doc = TextLoader(self.file).load()
        return doc[0].page_content