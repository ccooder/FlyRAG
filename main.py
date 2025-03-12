#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/12 13:51
import json

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

@tool
def sum_num(numbers: list[int]):
    '''
    计算所有数字的和
    :param numbers: 数字列表
    :return: 所有数字的和
    '''
    return sum(numbers)

tools = {'sum_num': sum_num}

class CaseInfo(BaseModel):
    year: int = Field(description="年份")
    name: str = Field(description="申请人")
    case_num: str = Field(description="案号")
class Date(BaseModel):
    year: int = Field(description="年份")
    month: int = Field(description="月份")
    day: int = Field(description="日期")

load_dotenv()
base_url = os.getenv('OPENAI_API_BASE')
llm = ChatOpenAI(base_url=base_url, model='Qwen/Qwen2.5-72B-Instruct', temperature=0)
llm_with_tools = llm.bind_tools([sum_num])
parser = PydanticOutputParser(pydantic_object=Date)

chain = (llm_with_tools)

prompt_template = PromptTemplate.from_template("现在的时间是{current_time}")

messages = [
    SystemMessage(content="提取用户输入的案件信息，年份、申请人、案号"),
    HumanMessage(content="帮我找一下张三2025年的206号案件")
]

messages = [
    SystemMessage(content=f"提取用户输入的日期信息{parser.get_format_instructions()}"),
    HumanMessage(content=prompt_template.format(current_time="2025年3月12日"))
]

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你现在是一个数学家"),
    HumanMessage(content="{i}")
])


chain = ({'i': RunnablePassthrough()} | chat_prompt | llm_with_tools)
# 初始化对话历史
message_history = InMemoryChatMessageHistory()
chain_with_history = RunnableWithMessageHistory(chain, lambda session_id : message_history, input_messages_key='input', history_messages_key='history')
response = chain_with_history.invoke({'input': '桌子上有两个桃，四个香蕉，一本书，一共有几个水果？'}, config={"configurable": {"session_id": "user123"}})
message_history.add_messages(response)
print(json.dumps(response.tool_calls, ensure_ascii=False))
for tool_call in response.tool_calls:
    tool = tools.get(tool_call['name'])
    tool_msg = tool.invoke(tool_call)
    message_history.append(tool_msg)

response = llm_with_tools.invoke(message_history.messages)
print(response)
