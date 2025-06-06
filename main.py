#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/12 13:51
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from common.redis_client import RedisClient
from flyrag.api import document, knowledge_base, model, chunk_config, retrival_config, document_chunk
from flyrag.api import file
from flyrag.task.task_dispatcher import TaskDispatcher


async def startup():
    await TaskDispatcher.start_pipeline()


async def shutdown():
    await TaskDispatcher.stop_pipeline()
    await RedisClient().close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await startup()
    yield
    # Clean up the ML models and release the resources
    await shutdown()


app = FastAPI(lifespan=lifespan)

# 添加 CORS 中间件（可选）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(file.router)
app.include_router(knowledge_base.router)
app.include_router(document.router)
app.include_router(document_chunk.router)
app.include_router(model.router)
app.include_router(chunk_config.router)
app.include_router(retrival_config.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
