#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 11:14
from flyrag.module.document import BaseParser
from langchain_community.document_loaders import Docx2txtLoader


class DocxParser(BaseParser):
    def parse(self):
        doc = Docx2txtLoader(self.file).load()
        return doc[0].page_content