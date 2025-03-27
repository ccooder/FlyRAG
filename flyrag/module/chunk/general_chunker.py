#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/26 15:32
import json

from flyrag.module.chunk import BaseChunker
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


class GeneralChunker(BaseChunker):
    def chunk(self):
        print(self.chunk_config)
        print(self.content)
        cts = CharacterTextSplitter(separator=self.chunk_config.delimiters, chunk_size=self.chunk_config.chunk_size,
                                    chunk_overlap=self.chunk_config.chunk_overlap)
        print(cts.__dict__)
        chunks = cts.split_text(self.content)
        print(chunks[0])
        print(len(chunks))
        pass
