import threading
import time
import logging

from common import REDIS_LOCK_SNOWFLAKE
from common.redis_client import RedisClient


class Snowflake(object):
    __instance = None
    __is_first = True

    def __new__(cls, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化Snowflake ID生成器
        :param datacenter_id: 数据中心ID，取值范围0-31
        :param worker_id: 工作节点ID，取值范围0-31
        :param sequence: 序列号，取值范围0-4095
        """
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        if Snowflake.__is_first:
            Snowflake.__is_first = False
            self.sequence = sequence
            self.rc = RedisClient()
            # 起始时间戳，可以自定义为服务启动时间
            self.twepoch = 1609459200000  # 2021-01-01 00:00:00

            # ID位数分配
            self.worker_id_bits = 5
            self.datacenter_id_bits = 5
            self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
            self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
            self.sequence_bits = 12

            # 移位偏移计算
            self.worker_id_shift = self.sequence_bits
            self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
            self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
            self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

            # 上次生成ID的时间戳
            self.last_timestamp = -1

            # 参数检查
            if self.worker_id > self.max_worker_id or self.worker_id < 0:
                raise ValueError(f"worker Id can't be greater than {self.max_worker_id} or less than 0")
            if self.datacenter_id > self.max_datacenter_id or self.datacenter_id < 0:
                raise ValueError(f"datacenter Id can't be greater than {self.max_datacenter_id} or less than 0")

    def _til_next_millis(self, last_timestamp):
        """
        阻塞到下一个毫秒，直到获得新的时间戳
        :param last_timestamp: 上次生成ID的时间戳
        :return: 当前时间戳
        """
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def _time_gen(self):
        """
        返回以毫秒为单位的当前时间戳
        :return: 当前时间戳
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取下一个ID
        :return: Snowflake ID
        """
        if self.rc.acquire_lock(REDIS_LOCK_SNOWFLAKE):
            try:
                timestamp = self._time_gen()

                if timestamp < self.last_timestamp:
                    logging.error(f"clock is moving backwards. Rejecting requests until {self.last_timestamp}")
                    raise Exception(f"InvalidSystemClock")

                if timestamp == self.last_timestamp:
                    self.sequence = (self.sequence + 1) & self.sequence_mask
                    if self.sequence == 0:
                        timestamp = self._til_next_millis(self.last_timestamp)
                else:
                    self.sequence = 0

                self.last_timestamp = timestamp

                return ((timestamp - self.twepoch) << self.timestamp_left_shift) | \
                    (self.datacenter_id << self.datacenter_id_shift) | \
                    (self.worker_id << self.worker_id_shift) | \
                    self.sequence
            finally:
                self.rc.release_lock(REDIS_LOCK_SNOWFLAKE)



# 示例用法
if __name__ == "__main__":
    for i in range(10):
        snowflake = Snowflake(worker_id=1, datacenter_id=1)
        print(snowflake.get_id())
