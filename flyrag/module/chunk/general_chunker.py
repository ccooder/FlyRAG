#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/26 15:32
import json

from flyrag.module.chunk import BaseChunker
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


class GeneralChunker(BaseChunker):
    def chunk(self):
        cts = RecursiveCharacterTextSplitter(separators=[self.chunk_config.delimiters, '\n'],
                                             chunk_size=self.chunk_config.chunk_size,
                                             chunk_overlap=self.chunk_config.chunk_overlap)
        chunks = cts.split_text(self.content)
        return chunks
