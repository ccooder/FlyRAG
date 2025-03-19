#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/14 12:36
import os
from typing import Union, Type

from dotenv import load_dotenv
from sqlalchemy import Select
from sqlmodel import create_engine, Session
from urllib.parse import quote_plus

from flyrag.api.entity import QueryEntity, Entity


class MysqlClient(object):
    __instance = None
    __is_first = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if MysqlClient.__is_first:
            MysqlClient.__is_first = False
            load_dotenv()
            host = os.getenv('MYSQL_HOST')
            user = os.getenv('MYSQL_USER')
            password = os.getenv('MYSQL_PASSWORD')
            self.__engine = create_engine(f"mysql+mysqlconnector://{user}:{quote_plus(password)}@{host}/fly_rag",
                                          echo=True)

    def get_session(self):
        with Session(self.__engine) as session:
            yield session

    @staticmethod
    def fill_statement(statement, cls: Type[Entity], qe: QueryEntity):
        if qe.id:
            statement = statement.where(cls.id == qe.id)
        if qe.status:
            statement = statement.where(cls.status == qe.status)
        if qe.is_deleted is not None:
            statement = statement.where(cls.is_deleted == qe.is_deleted)
        if qe.start_time:
            statement = statement.where(cls.create_time >= qe.start_time)
        if qe.end_time:
            statement = statement.where(cls.create_time <= qe.end_time)
        return statement
