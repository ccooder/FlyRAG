#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 10:47
from enum import Enum
from typing import Type, Generic

from langchain.retrievers.document_compressors.cross_encoder import BaseCrossEncoder
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from common.mysql_client import MysqlClient
from flyrag.api.entity import Model
from flyrag.api.service.model_service import ModelService
from flyrag.module.embedding.xinference_embedding import XinferenceEmbedding
from flyrag.module.reranker.siliconflow_cross_encoder import SiliconFlowCrossEncoder
from flyrag.module.reranker.xinference_cross_encoder import XinferenceCrossEncoder

name = 'module'


class ModelProvider(Enum):
    OpenAI_Compatible = 1
    Xinference = 2
    SiliconFlow = 3



class ModelProviderContext(object):
    def __init__(self, model: Model):
        self.__model = model

    def get_embedding(self) -> Embeddings:
        if self.__model.provider == ModelProvider.OpenAI_Compatible.value:
            return OpenAIEmbeddings(base_url=self.__model.base_url, api_key=SecretStr(self.__model.api_key),
                                    model=self.__model.name)
        elif self.__model.provider == ModelProvider.Xinference.value:
            return XinferenceEmbedding(self.__model.base_url, self.__model.uid)

    def get_cross_encoder(self) -> BaseCrossEncoder:
        if self.__model.provider == ModelProvider.Xinference.value:
            return XinferenceCrossEncoder(self.__model.base_url, self.__model.uid)
        elif self.__model.provider == ModelProvider.SiliconFlow.value:
            return SiliconFlowCrossEncoder(self.__model.base_url, self.__model.api_key, self.__model.name)
