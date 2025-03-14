#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 17:28

from fastapi import APIRouter


router = APIRouter(prefix='/document', tags=["document"])

@router.post("/create")
async def create_doc():
   pass