#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/27 14:55
import sys
from typing import Set

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

import common
from common.mysql_client import MysqlClient
from flyrag.api.service.document_chunk_service import DocumentChunkService


class LLM(object):

    def __init__(self, temperature=0.3, model='Qwen/Qwen2.5-72B-Instruct'):
        load_dotenv()
        base_url = os.getenv('OPENAI_API_BASE')
        self.__llm = ChatOpenAI(
            base_url=base_url,
            temperature=temperature,
            model=model
        )

    def determine_qa(self, text):
        prompt = PromptTemplate.from_file(f'{common.root_path()}/prompt/determine_qa_prompt.md')
        messages = [
            SystemMessage(content=prompt.template),
            HumanMessage(content=text)
        ]
        response = self.__llm.invoke(messages)
        return response

    def query_rewrite(self, text):
        prompt = PromptTemplate.from_file(f'{common.root_path()}/prompt/query_rewrite_prompt.md')
        messages = [
            SystemMessage(content=prompt.template),
            HumanMessage(content=text)
        ]
        response = self.__llm.invoke(messages)
        return response

    def rag(self, query):
        from flyrag.module.retrival.rag_fusion_retriever import RagFusionRetriever
        documents = RagFusionRetriever(kb_id=558200461551865856, query=query).retrieve()
        chunk_ids = set()
        for document, score in documents:
            chunk_id = document.metadata['chunk_id']
            chunk_ids.add(chunk_id)
        chunks = DocumentChunkService.get_chunks(list(chunk_ids), session=next(MysqlClient().get_session()))

        prompt = PromptTemplate.from_file(f'{common.root_path()}/prompt/chat_prompt.md')

        chain = RunnablePassthrough() | prompt | self.__llm

        return chain.invoke({'query': query, 'context': chunks})


if __name__ == '__main__':
    llm = LLM()
    print(llm.query_rewrite('什么情况下能申请劳动仲裁'))
