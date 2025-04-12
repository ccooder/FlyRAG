#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/4/12 14:26
import os
from typing import List, Tuple

import requests
from dotenv import load_dotenv
from langchain.retrievers.document_compressors.cross_encoder import BaseCrossEncoder
from pydantic import BaseModel


class SiliconFlowCrossEncoder(BaseCrossEncoder, BaseModel):

    def __init__(self, base_url: str, api_key: str, model_name: str, **kwargs):
        super().__init__(**kwargs)
        self.__base_url = base_url
        self.__api_key = api_key
        self.__model_name = model_name

    def score(self, text_pairs: List[Tuple[str, str]]) -> List[float]:
        query = text_pairs[0][0]
        corpus = [text_pair[1] for text_pair in text_pairs]
        headers = {
            'Authorization': f'Bearer {self.__api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.__model_name,
            'query': query,
            'documents': corpus,
            'top_n': len(corpus),
            'return_documents': False,
            'max_chunks_per_doc': 1024,
            'overlap_tokens': 80
        }
        response = requests.post(self.__base_url, json=payload, headers=headers).json()
        scores = map(lambda x: x['relevance_score'], response['results'])
        return scores
