#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 11:11
from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy import table
from sqlmodel import SQLModel, Field

from common.snowflake import Snowflake

name = "entity"

# 序列化
model_config = ConfigDict(
    from_attributes=True,
    json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"),
                   int: lambda o: o if o < 0x20000000000000 else str(o)}
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


# 知识库
class KnowledgeBase(Entity, table=True):
    """
    知识库实体
    """
    __tablename__ = 'fr_knowledge_base'
    name: str = Field(default=None, max_length=64)
    profile: str = Field(default=None, max_length=255)


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


# 文档
class Document(Entity, table=True):
    """
    知识库实体
    """
    __tablename__ = 'fr_document'
    kb_id: int = Field(default=None)
    name: str = Field(default=None)
    original_name: str = Field(default=None)
    size: int = Field(default=None)
    obj_name: str = Field(default=None)
    char_count: int = Field(default=None)
