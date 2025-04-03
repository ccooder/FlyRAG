#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 11:11
import functools
import json
import sys
import time
import hashlib
from datetime import datetime, date

from enum import Enum

from httpx._urlparse import urlparse

name = 'common'

DEFAULT_BUCKET_NAME = 'fly-rag'
DEFAULT_WEAVIATE_COLLECTION = 'fly_rag'
SALT = 'ZERO_JX_DEEP_SEARCH:'
REQ_CHECK = "REQ_CHECK"


class FlyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            if obj > 0x20000000000000:
                return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


# 日志模块
import logging.config
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# 获取项目根目录
import inspect
from typing import Set


def does_file_path_contain_path_component(cur_file_dir: str):
    cur_file_components = os.path.normpath(cur_file_dir).split(os.sep)
    possible_roots = set()
    for path in sys.path:
        possible_root_dir = True
        for cur_file_comp, comp in zip(cur_file_components, os.path.normpath(path).split(os.sep)):
            if cur_file_comp != comp:
                possible_root_dir = False
        if possible_root_dir:
            possible_roots.add(path)
    return possible_roots


def shortest_possible_root(possible_roots: Set[str]):
    shortest_root_len = None
    shortest_root = None
    for root in possible_roots:
        comps = os.path.normpath(root).split(os.sep)
        comp_len = len(comps)
        if shortest_root_len is None or comp_len < shortest_root_len:
            shortest_root_len = comp_len
            shortest_root = root
    return shortest_root


def root_path(ignore_cwd=True):
    """
    :param ignore_cwd: ignore the current working directory for deriving the root path
    :return returns project root path:
    :rtype: str
    """
    filename = os.path.abspath(inspect.stack()[1][0].f_code.co_filename)
    cur_file_dir = os.path.dirname(filename)
    if not ignore_cwd and cur_file_dir == os.path.abspath(os.getcwd()):
        return cur_file_dir
    possible_roots = does_file_path_contain_path_component(cur_file_dir)
    return shortest_possible_root(possible_roots)


# 创建日志目录
logs_folder = root_path() + '/logs'
if not os.path.exists(logs_folder):
    os.mkdir(logs_folder)

# 日志配置字典
logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - [%(processName)s-%(threadName)s] [%(name)s/%(filename)s:%(lineno)d] - %(message)s'
        }
    },
    'handlers': {
        'root': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': f'{logs_folder}/app.log',
            'when': 'midnight',
            'interval': 1,  # Rotate daily
            'backupCount': 7,  # Keep 7 days of logs
            'encoding': 'UTF-8',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'handlers': ['root', 'console'],
        'level': 'INFO',
    },
}
# 创建日志配置字典
logging.config.dictConfig(logging_config)


def get_logger():
    module_name = ''
    # Get the caller's frame
    caller_frame = inspect.stack()[1]
    # Extract the module name from the frame
    caller_module = inspect.getmodule(caller_frame[0])
    if caller_module:
        module_name = caller_module.__name__
    else:
        module_name = '__main__'

    l = logging.getLogger(module_name)
    return l


def is_valid_url(url: str) -> bool:
    """Check if the url is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_char_count(text: str) -> int:
    space_count = sum(1 for c in text if c.isspace())
    char_count = len(text) - space_count
    return char_count
