#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 11:14
import re
from io import BytesIO

import fitz
from fengluU import exec_time
from tqdm import tqdm

from flyrag.module.document import BaseParser
from langchain_community.document_loaders import PyMuPDFLoader


class PdfParser(BaseParser):
    @exec_time
    def parse(self):
        doc = PyMuPDFLoader(self.file, mode='single').load()
        return doc[0].page_content
