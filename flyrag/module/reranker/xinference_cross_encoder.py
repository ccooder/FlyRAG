#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/8 17:29
from typing import List, Tuple, Any

from langchain.retrievers.document_compressors.cross_encoder import BaseCrossEncoder
from pydantic import BaseModel
from xinference_client.client.restful.restful_client import Client


class XinferenceCrossEncoder(BaseCrossEncoder, BaseModel):

    def __init__(self, base_url: str, model_uid: str, **kwargs):
        super().__init__(**kwargs)
        self.__client = Client(base_url)
        self.__model_uid = model_uid

    def score(self, text_pairs: List[Tuple[str, str]]) -> List[float]:
        query = text_pairs[0][0]
        corpus = [text_pair[1] for text_pair in text_pairs]
        response = self.__client.get_model(self.__model_uid).rerank(corpus, query)
        scores = map(lambda x: x['relevance_score'], response['results'])
        return scores

