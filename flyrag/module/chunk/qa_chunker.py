#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/27 14:50
from flyrag.module.chunk import BaseChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter


class QaChunker(BaseChunker):
    def chunk(self):
        separator = r'问[:：]|Q[:：]'
        cts = RecursiveCharacterTextSplitter(separators=[separator], keep_separator='start',
                                             is_separator_regex=True,
                                             chunk_size=self.chunk_config.chunk_size,
                                             chunk_overlap=self.chunk_config.chunk_overlap)
        chunks = cts.split_text(self.content)
        return chunks
