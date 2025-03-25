#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 11:11
from datetime import datetime
from typing import List, Union

import pydantic
from pydantic import ConfigDict, BaseModel
from sqlalchemy import table
from sqlmodel import SQLModel, Field

from common.snowflake import Snowflake

name = "entity"

# 序列化
model_config = ConfigDict(
    from_attributes=True,
    json_encoders={datetime: lambda dt: '' if dt is None else dt.strftime("%Y-%m-%d %H:%M:%S"),
                   int: lambda o: '' if o is None else o if o < 0x20000000000000 else str(o)}
)


class Entity(SQLModel):
    model_config = model_config
    id: int = Field(default_factory=Snowflake(datacenter_id=1, worker_id=1).get_id, primary_key=True)
    create_time: datetime = Field(default=datetime.now())
    update_time: datetime = Field(default=datetime.now())
    status: int = Field(default=1)
    is_deleted: int = Field(default=0)


class UpdateEntity(SQLModel):
    id: int = Field(default=None)
    update_time: datetime = Field(default=datetime.now())


class DeleteEntity(SQLModel):
    id: int = Field(default=None)
    is_deleted: int = Field(default=1)


class QueryEntity(SQLModel):
    id: int = Field(default=None)
    is_deleted: int = Field(default=0)
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)
    key: str = Field(default=None)
    status: int = Field(default=None)

# 文档
class Document(Entity, table=True):
    """
    文档实体
    """
    __tablename__ = 'fr_document'
    model_config = model_config
    kb_id: int = Field(default=None)
    name: str = Field(default=None)
    original_name: str = Field(default=None)
    chunk_mode: int = Field(default=None)
    size: int = Field(default=None)
    obj_name: str = Field(default=None)
    char_count: int = Field(default=0)
    pause: int = Field(default=0)

class DocumentCreate(BaseModel):
    """
    文档实体-创建
    """
    kb_id: int = pydantic.Field(..., alias="kbId")
    docs: List[Document] = Field(default=None)

class DocumentQuery(QueryEntity):
    """
    文档实体-查询
    """
    kb_id: int = Field(...)

class DocumentUpdate(UpdateEntity):
    """
    文档实体-更新
    """
    name: str = Field(default=None)
    mode: int = Field(default=None)
    status: int = Field(default=None)

# 切片配置
class ChunkConfig(Entity, table=True):
    """
    切片配置实体
    """
    __tablename__ = 'fr_chunk_config'
    target_id: int = Field(default=None)
    type: int = Field(default=None)
    embedding_model_id: int = Field(...)
    mode: int = Field(default=1)
    chunk_size: int = Field(default=512)
    chunk_overlap: int = Field(default=200)
    delimiters: str = Field(default='\n\n')

# 知识库
class KnowledgeBase(Entity, table=True):
    """
    知识库实体
    """
    __tablename__ = 'fr_knowledge_base'
    name: str = Field(default=None, max_length=64)
    profile: str = Field(default=None, max_length=255)

class KnowledgeBaseCreate(Entity):
    """
    知识库实体
    """
    name: str = Field(default=None, max_length=64)
    profile: str = Field(default=None, max_length=255)
    docs: List[Document] = Field(default=None)
    chunk_config: ChunkConfig = Field(default=None)


    def get_kb(self):
        return KnowledgeBase(**self.model_dump())


class KnowledgeBaseUpdate(UpdateEntity):
    """
    知识库实体-更新
    """
    name: str = Field(default=None, max_length=64)
    profile: str = Field(default=None, max_length=255)


class KnowledgeBaseQuery(QueryEntity):
    """
    知识库实体-查询
    """
    name: str = Field(default=None, max_length=64)
    profile: str = Field(default=None, max_length=255)


# 模型
class Model(Entity, table=True):
    """
    模型实体
    """
    __tablename__ = 'fr_model'
    name: str = Field(default=None, max_length=64)
    uid: str = Field(default=None, max_length=32)
    base_url: str = Field(default=None, max_length=255)
    api_key: str = Field(default=None, max_length=255)
    context_length: int = Field(default=4096)
    type: int = Field(default=1)

class ModelQuery(QueryEntity):
    """
    模型实体-查询
    """
    type: int = Field(default=1)


