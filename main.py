#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/12 13:51

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import file
from api import knowledge_base

app = FastAPI()

# 添加 CORS 中间件（可选）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(file.router)
app.include_router(knowledge_base.router)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

