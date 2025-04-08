#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/31 17:12
import os
from contextlib import contextmanager

from dotenv import load_dotenv
import weaviate
from weaviate.auth import Auth


class WeaviateClient(object):
    __instance = None
    __is_first = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if WeaviateClient.__is_first:
            WeaviateClient.__is_first = False
            load_dotenv()
            self.__host = os.getenv('WEAVIATE_HOST')
            self.__port = int(os.getenv('WEAVIATE_PORT'))
            self.__grpc_port = int(os.getenv('WEAVIATE_GRPC_PORT'))
            self.__api_key = os.getenv('WEAVIATE_API_KEY')

    def get_client(self):
        return weaviate.connect_to_local(
            host=self.__host,
            port=self.__port,
            grpc_port=self.__grpc_port,
            auth_credentials=Auth.api_key(self.__api_key)
        )

if __name__ == '__main__':
    with WeaviateClient().get_client() as client:
        client.is_ready()
        client.collections.delete_all()