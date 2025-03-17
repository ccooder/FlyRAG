#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/17 15:25
from enum import Enum, auto

class DocumentStatus(Enum):
    QUEUEING = 1,
    INDEXING = 2,
    AVAILABLE = 3,
    DISABLED = 0
