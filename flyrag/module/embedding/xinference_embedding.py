#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/31 15:11
from langchain_core.embeddings import Embeddings
from xinference_client import RESTfulClient as Client


class XinferenceEmbedding(Embeddings):
    __instance = None
    __is_first = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, base_url: str, model_uid: str):
        if XinferenceEmbedding.__is_first:
            XinferenceEmbedding.__is_first = False
            self.__client = Client(base_url)
        self.__model_uid = model_uid


    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.__client.get_model(self.__model_uid).create_embedding(
            input=texts,
        )
        return [x['embedding'] for x in response['data']]

    def embed_query(self, text: str) -> list[float]:
        response = self.__client.get_model(self.__model_uid).create_embedding(
            input=text,
        )
        return response['data'][0]['embedding']
