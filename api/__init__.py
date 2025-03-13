#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 22:05

from pydantic import BaseModel, Field


class R(BaseModel):
    code: int = Field(200, description="返回码")
    data: object = Field(None, description="返回数据")
    msg: str = Field("操作成功", description="返回信息")
    status: bool = Field(True, description="返回状态")

    @classmethod
    def ok(cls, msg: str = "操作成功", data=None):
        return R(code=200, data=data, msg=msg, status=True).__dict__

    @classmethod
    def fail(cls, msg: str):
        return R(code=400, data=None, msg=msg, status=False).__dict__