#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import json
import time

from redis.asyncio import Redis

import common
from common.minio_client import MinioClient
from common.mysql_client import MysqlClient
from common.redis_client import RedisClient
from flyrag.api.entity import Entity, Document, DocumentUpdate, DocumentChunk, DocumentContent
from flyrag.api.enums import DocumentStatus
from flyrag.api.service.chunk_config_service import ChunkConfigService
from flyrag.api.service.document_chunk_service import DocumentChunkService
from flyrag.api.service.document_content_service import DocumentContentService
from flyrag.api.service.document_service import DocumentService
from flyrag.module.chunk import ChunkerContext, ChunkMode
from flyrag.module.document import DocumentParserContext
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT, PIPELINE_LIMIT, REDIS_KEY_PIPELINE_QUEUE, \
    REDIS_KEY_PIPELINE_FLAG

name = 'chunking'


class ChunkingPipeline(TaskPipeline):
    async def start(self):
        while int((await self._redis.get(REDIS_KEY_PIPELINE_FLAG)).decode('utf-8')):
            if await super().is_over_limit(name):
                continue

            # Lua 脚本
            script = """
                    local doc = redis.call('RPOP', KEYS[1])
                    if doc then
                        redis.call('INCR', KEYS[2])
                    end
                    return doc
                    """

            # 执行 Lua 脚本
            doc_redis = await self._redis.eval(script, 2, REDIS_KEY_PIPELINE_QUEUE.format(name),
                                               REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
            if doc_redis is None:
                time.sleep(1)
                continue
            doc = Document(**json.loads(doc_redis))
            # 判断任务是否暂停
            if await super().is_pause(doc.id):
                # 若任务暂停放回队列底部并且将执行中的数量-1
                await super().put_back(name, doc_redis)
                continue

            # 执行任务
            try:
                await self.execute(doc)
            except Exception as e:
                common.get_logger().error('执行切片失败,将任务重新放回队列底部。{}', e)
                await super().change_status(doc, name, DocumentStatus.QUEUEING)
                await super().put_back(name, doc_redis)

    async def execute(self, doc: Document):
        # 初始化文档处理进度
        await super().incr_progress(doc.id, 0)
        if not await super().change_status(doc, name, DocumentStatus.INDEXING):
            return
        file_path = MinioClient().get_presigned_url(common.DEFAULT_BUCKET_NAME, doc.obj_name)
        content = DocumentParserContext.do_parse(file_path)
        session = next(MysqlClient().get_session())
        # 统计字符数，去除空格，保存至文档信息
        DocumentService.update_doc(DocumentUpdate(id=doc.id, char_count=common.get_char_count(content)), session)
        # 将文档内容存入数据库
        DocumentContentService.create_content(DocumentContent(doc_id=doc.id, content=content), session)
        # 解析完文档，进度增加0.05
        await super().incr_progress(doc.id, 0.05)
        # 获取文档的切片配置
        chunk_config = ChunkConfigService().get_chunk_config(doc.id, next(MysqlClient().get_session()))
        # 不同的切片模式，返回的切片数据结构不一样
        if chunk_config.mode == ChunkMode.General.value:
            chunks = ChunkerContext.do_chunk(content, doc, chunk_config)
            # 保存切片数量至文档信息
            session = next(MysqlClient().get_session())
            try:
                DocumentService.update_doc(DocumentUpdate(id=doc.id, chunk_count=len(chunks)), session,
                                           autocommit=False)
                # 保存切片到数据库
                doc_chunks = [
                    DocumentChunk(doc_id=int(doc.id), chunk=chunk, chunk_no=i + 1,
                                  char_count=common.get_char_count(chunk)) for
                    i, chunk in enumerate(chunks)]
                DocumentChunkService.create_chunks(doc_chunks, session)
                session.commit()
            except Exception as e:
                common.get_logger().error('保存切片失败{}', e)
                session.rollback()
                return

        # 切片入库后进度增加0.05
        await super().incr_progress(doc.id, 0.05)
        # 切片入库后，执行任务数-1
        await self._redis.decr(REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
