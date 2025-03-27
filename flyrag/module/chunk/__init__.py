#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 10:49
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from flyrag.api.entity import Document, ChunkConfig
from flyrag.llm import LLM

class BaseChunker(ABC):
    """
        文档切片器父类
    """

    def __init__(self, content: str = None, doc: Document = None, chunk_config: ChunkConfig = None):
        self.__content = content
        self.__doc = doc
        self.__chunk_config = chunk_config

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content: str):
        self.__content= content

    @property
    def doc(self):
        return self.__doc

    @doc.setter
    def doc(self, doc: int):
        self.__doc = doc

    @property
    def chunk_config(self):
        return self.__chunk_config

    @chunk_config.setter
    def chunk_config(self, chunk_config: int):
        self.__chunk_config = chunk_config

    @abstractmethod
    def chunk(self):
        """
        切片文档
        """
        pass

class ChunkMode(Enum):
    """
    切片模式枚举
    """
    General = 1
    Small2Big = 2
    Mixed = 3

class ChunkerContext(object):
    """
    文档切片器上下文
    """

    @staticmethod
    def do_chunk(content: str, doc: Document, chunk_config: ChunkConfig) -> Any | None:
        # 先判断文档结构是否问答形式
        llm = LLM()
        result = llm.determine_qa(content[:100])
        if result.content == '1':
            from flyrag.module.chunk.qa_chunker import QaChunker
            return QaChunker(content, doc, chunk_config).chunk()
        else:
            chunk_mode = ChunkMode(chunk_config.mode)
            # 动态加载切片器
            from flyrag.module.chunk.general_chunker import GeneralChunker
            chunker = eval(f'{chunk_mode.name}Chunker(content, doc, chunk_config)')
            return chunker.chunk()

if __name__ == '__main__':
    text = '''
    '''
    ChunkerContext.do_chunk(text, None, ChunkConfig(mode=ChunkMode.General.value, chunk_size=500, chunk_overlap=100))