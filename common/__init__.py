#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 11:11
import functools
import json
import time
import hashlib
from datetime import datetime, date

from enum import Enum

name = 'common'

DEFAULT_BUCKET_NAME = 'fly-rag'
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

# 创建日志目录
logs_folder = 'logs'
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

import inspect


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