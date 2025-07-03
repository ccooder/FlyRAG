#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 14:35
import os
import time

import redis
from dotenv import load_dotenv
from redis import WatchError
from redis.asyncio import Redis, ConnectionPool


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
            url = f'redis://:{password}@{host}/{database}'
            self.__apool = ConnectionPool.from_url(url)
            self.__pool = redis.ConnectionPool.from_url(url)

    async def close(self):
        await self.__apool.disconnect()
        self.__pool.disconnect()

    def get_aredis(self):
        return Redis(connection_pool=self.__apool)

    def get_redis(self):
        return redis.Redis(connection_pool=self.__pool)


    async def delete_keys_with_prefix(self, prefix):
        aredis = self.get_aredis()
        cursor = '0'
        while cursor != 0:
            cursor, keys = await aredis.scan(cursor=cursor, match=f"{prefix}*", count=1000)
            if keys:
                await aredis.delete(*keys)

    def acquire_lock(self, lock_name, blocking=True, timeout=10, expire=10):
        r = self.get_redis()
        end = None
        if timeout:
            end = time.time() + timeout

        while True:
            if r.set(lock_name, 1,  ex=expire, nx=True):
                return True
            elif not blocking:
                return False

            if end and time.time() > end:
                return False

            time.sleep(0.001)

    def release_lock(self, lock_name):
        r = self.get_redis()
        pipe = r.pipeline()
        while True:
            try:
                pipe.watch(lock_name)
                if int(pipe.get(lock_name).decode('utf-8')) == 1:
                    pipe.multi()
                    pipe.delete(lock_name)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except WatchError as e:
                pass
        return False
