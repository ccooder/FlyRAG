#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/27 14:55
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

class LLM(object):
    def __init__(self):
        load_dotenv()
        base_url = os.getenv("OPENAI_API_BASE")
        print(base_url)
        self.__llm = ChatOpenAI(
            base_url=base_url,
            temperature=0.3,
            model="Qwen/Qwen2.5-72B-Instruct"
        )

    def chat(self, text):
        prompt = PromptTemplate.from_file("../../prompt/determine_qa_prompt.md")
        messages = [
            SystemMessage(content=prompt.template),
            HumanMessage(content=text)
        ]
        response = self.__llm(messages)
        return response.content

    def determine_qa(self, text):
        prompt = PromptTemplate.from_file("../../../prompt/determine_qa_prompt.md")
        messages = [
            SystemMessage(content=prompt.template),
            HumanMessage(content=text)
        ]
        response = self.__llm.invoke(messages)
        return response
    pass