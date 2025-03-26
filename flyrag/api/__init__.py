#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 22:05
from collections.abc import Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field


class R(BaseModel):
    code: int = Field(200, description="返回码")
    data: object = Field(None, description="返回数据")
    msg: str = Field("操作成功", description="返回信息")
    status: bool = Field(True, description="返回状态")

    @classmethod
    def ok(cls, msg: str = "操作成功", data=None):
        return jsonable_encoder(R(code=200, data=data, msg=msg, status=True))

    @classmethod
    def fail(cls, msg: str):
        return R(code=400, data=None, msg=msg, status=False).__dict__

class Page(BaseModel):
    total: int = Field(0, description="总数")
    current: int = Field(1, description="当前页")
    size: int = Field(10, description="每页大小")
    pages: int = Field(0, description="总页数")
    records: Sequence = Field([], description="数据")

    @classmethod
    def of(cls, current: int, size: int, total: int, records: Sequence):
        pages = total // size + 1 if total % size else total // size
        return Page(total=total, pages=pages, current=current, size=size, records=records)