#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/8 14:54
from fengluU import exec_time
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_core.load import loads
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_weaviate import WeaviateVectorStore

from common import DEFAULT_WEAVIATE_COLLECTION
from common.mysql_client import MysqlClient
from common.rrf import reciprocal_rank_fusion
from common.weaviate_client import WeaviateClient
from flyrag.api.service.chunk_config_service import ChunkConfigService
from flyrag.api.service.model_service import ModelService
from flyrag.llm import LLM
from flyrag.module.embedding.xinference_embedding import XinferenceEmbedding
from flyrag.module.reranker.xinference_cross_encoder import XinferenceCrossEncoder


class RagFusionRetriever(object):

    def __init__(self, kb_id: int, query: str, top_k=10, k=10):
        self.__k = k
        self.__top_k = top_k
        self.__kb_id = kb_id
        self.__query = query
        self.__llm = LLM()

    @exec_time
    def retrieve(self):
        generate_queries = (
                RunnablePassthrough() | self.__llm.query_rewrite | StrOutputParser() | loads
        )
        chunk_config = ChunkConfigService.get_chunk_config(self.__kb_id, next(MysqlClient().get_session()))
        embedding_model = ModelService.get_model(chunk_config.embedding_model_id, next(MysqlClient().get_session()))
        reranker_model = ModelService.get_model(chunk_config.reranker_model_id, next(MysqlClient().get_session()))
        embedding = XinferenceEmbedding(base_url=embedding_model.base_url, model_uid=embedding_model.uid)
        reranker = XinferenceCrossEncoder(base_url=reranker_model.base_url, model_uid=reranker_model.uid)
        with WeaviateClient().get_client() as weaviate_client:
            compressor = CrossEncoderReranker(model=reranker, top_n=3)

            wvs = WeaviateVectorStore(client=weaviate_client, index_name=DEFAULT_WEAVIATE_COLLECTION, text_key='text',
                                      embedding=embedding)
            retriever = wvs.as_retriever(search_kwargs={'k': self.__top_k})
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retriever
            )
            chain = (
                    generate_queries
                    | compression_retriever.map()
                    | reciprocal_rank_fusion
            )
            print(chain.invoke(self.__query))

if __name__ == '__main__':
    RagFusionRetriever(kb_id=559627226199494656, query="我的案件结案了吗").retrieve()