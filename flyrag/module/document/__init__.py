#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 10:49
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from pathlib import Path
import regex
import requests

import common


class BaseParser(ABC):
    """
        文档解析器父类
    """

    def __init__(self, file: str = None, start_page: int = None, end_page: int = None):
        self.__file = file
        self.__start_page = start_page
        self.__end_page = end_page

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, file: str):
        self.__file = file

    @property
    def start_page(self):
        return self.__start_page

    @start_page.setter
    def start_page(self, start_page: int):
        self.__start_page = start_page

    @property
    def end_page(self):
        return self.__end_page

    @end_page.setter
    def end_page(self, end_page: int):
        self.__end_page = end_page

    @abstractmethod
    def parse(self):
        '''
        解析文档
        '''
        pass


class DocumentFormat(Enum):
    """
    文档格式枚举
    """
    Pdf = 'pdf'
    Docx = 'docx'
    Excel = 'xlsx'
    Txt = 'txt|java|c|h|cpp|js|py|conf|ini|sh|md|markdown'
    # Markdown = 'md|markdown'
    Html = 'html'

    @staticmethod
    def of(file: str):
        file_path = Path(file)
        for v in DocumentFormat.__members__.values():
            if regex.search(rf'\.({v.value})\??', file_path.suffix):
                return v
        else:
            raise NotImplementedError(f'不支持的文件格式: {file_path.suffix}')


class DocumentParserContext(object):
    """
    文档解析器上下文
    """

    @staticmethod
    def do_parse(file: str, start_page: int = 0, end_page: int = 100000) -> Any | None:
        doc_format = DocumentFormat.of(file)
        if doc_format == DocumentFormat.Txt and common.is_valid_url(file):
            resp = requests.get(file)
            resp.encoding = 'utf-8'
            return resp.text
        # 动态加载解析器
        from flyrag.module.document.docx_parser import DocxParser
        from flyrag.module.document.pdf_parser import PdfParser
        from flyrag.module.document.txt_parser import TxtParser
        doc_parser = eval(f'{doc_format.name}Parser("{file}", {start_page}, {end_page})')
        return doc_parser.parse()

if __name__ == '__main__':
    print(DocumentParserContext.do_parse(fr'D:\WORK\doc\知识库文档\问题修复2025030902.pdf'))
    # print(DocumentParserContext.do_parse(fr'C:/Users/niufe/Desktop/test.pdf'))