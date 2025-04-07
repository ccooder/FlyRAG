#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:12
import json
import time
from copy import deepcopy

from langchain_weaviate import WeaviateVectorStore
from regex import regex

import common
from common import DEFAULT_WEAVIATE_COLLECTION
from common.mysql_client import MysqlClient
from common.weaviate_client import WeaviateClient
from flyrag.api.entity import DocumentChunk, DocumentChunkVid
from flyrag.api.service.chunk_config_service import ChunkConfigService
from flyrag.api.service.document_chunk_vid_service import DocumentChunkVidService
from flyrag.api.service.document_service import DocumentService
from flyrag.api.service.model_service import ModelService
from flyrag.module.embedding.xinference_embedding import XinferenceEmbedding
from flyrag.task import TaskPipeline, REDIS_KEY_PIPELINE_TASK_COUNT, \
    REDIS_KEY_PIPELINE_QUEUE, REDIS_KEY_DOC_EMBEDDING_PROGRESS, REDIS_KEY_DOC_PROGRESS, DocumentTaskStatus

name = 'embedding'


class EmbeddingPipeline(TaskPipeline):
    async def start(self):
        while await super().pipeline_flag():
            if await super().is_over_limit(name):
                continue
            # Lua 脚本
            script = """
                    local chunk = redis.call('RPOP', KEYS[1])
                    if chunk then
                        redis.call('INCR', KEYS[2])
                    end
                    return chunk
                    """

            # 执行 Lua 脚本
            chunk_redis = await self._redis.eval(script, 2, REDIS_KEY_PIPELINE_QUEUE.format(name),
                                                 REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
            if chunk_redis is None:
                time.sleep(1)
                continue
            chunk = DocumentChunk(**json.loads(chunk_redis))
            # 判断任务是否暂停
            if await super().is_pause(chunk.doc_id):
                # 若任务暂停放回队列底部并且将执行中的数量-1
                await super().put_back(name, chunk_redis)
                continue
            # 执行任务
            try:
                await self.execute(chunk)
            except Exception as e:
                common.get_logger().error('向量化失败,将任务重新放回队列底部。{}', e)
                await super().put_back(name, chunk_redis)
                continue

    async def execute(self, chunk: DocumentChunk):
        with WeaviateClient().get_client() as weaviate_client:
            session = next(MysqlClient().get_session())
            doc = DocumentService.get_doc(chunk.doc_id, session)
            # 获取向量模型配置
            chunk_config = ChunkConfigService.get_chunk_config(chunk.doc_id, session)
            model = ModelService.get_model(chunk_config.embedding_model_id, session)
            embedding = XinferenceEmbedding(model.base_url, model.uid)
            # 初始化 WeaviateVectorStore
            wvs = WeaviateVectorStore(client=weaviate_client, index_name=DEFAULT_WEAVIATE_COLLECTION, text_key='text',
                                      embedding=embedding)
            # 组装文本与Metadata
            texts = [chunk.chunk]
            metadata = {'doc_id': chunk.doc_id, 'chunk_id': chunk.id}
            metadatas = [metadata]
            if doc.is_qa == 1:
                pattern = r'(问[:：\s]|Q[:：\s])(.*?)\s(答[:：\s]|A[:：\s])'
                match = regex.finditer(pattern, chunk.chunk)
                questions = [m.group(2) for m in match]
                if len(questions) > 0:
                    for q in questions:
                        texts.append(q)
                        metadatas.append(deepcopy(metadata))
            # 向量入库
            vids = await wvs.aadd_texts(texts, metadatas)
            # 将向量IDs保存，以备后续删除
            vids_str = ','.join(vids)
            dcv = DocumentChunkVid(doc_id=chunk.doc_id, chunk_id=chunk.id, vids=vids_str)
            DocumentChunkVidService.create_chunk_vid([dcv], session)

            # 文档索引进度更新
            await super().incr_progress(chunk.doc_id, round(1 / doc.chunk_count * 0.9, 4))

            # 记录该文档的切片向量进度
            embedding_progress = await self._redis.incr(REDIS_KEY_DOC_EMBEDDING_PROGRESS.format(chunk.doc_id))
            if embedding_progress == doc.chunk_count:
                # 若切片向量进度等于切片总数，则将文档向量化进度置为1
                await self._redis.set(REDIS_KEY_DOC_PROGRESS.format(chunk.doc_id), 1)
                # 将文档向量化进度删除
                await self._redis.delete(REDIS_KEY_DOC_EMBEDDING_PROGRESS.format(chunk.doc_id))
                # 将文档交给调度
                from flyrag.task.task_dispatcher import TaskDispatcher
                await TaskDispatcher.dispatch_task([doc], DocumentTaskStatus.INDEXED)
            # 向量入库成功后执行任务数-1
            await self._redis.decr(REDIS_KEY_PIPELINE_TASK_COUNT.format(name))
