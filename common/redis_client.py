#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 14:35
import os

from dotenv import load_dotenv
from langchain_community.utilities.redis import get_client
from redis import Redis


class RedisClient(object):
    __instance = None
    __is_first = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if RedisClient.__is_first:
            RedisClient.__is_first = False
            load_dotenv()
            host = os.getenv('REDIS_HOST')
            password = os.getenv('REDIS_PASSWORD')
            database = os.getenv('REDIS_DATABASE')
            client = get_client(f"redis://:{password}@{host}/{database}")

            self.__redis = client
    def get_redis(self) -> Redis:
        return self.__redis

