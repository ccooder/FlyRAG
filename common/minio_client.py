#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 21:43
import common
import os
from abc import ABC

from minio import Minio, S3Error
from dotenv import load_dotenv


class MinioClient(ABC):
    __instance = None
    __is_first = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if MinioClient.__is_first:
            MinioClient.__is_first = False
            load_dotenv()
            endpoint = os.getenv('MINIO_ENDPOINT')
            access_key = os.getenv('MINIO_ACCESS_KEY')
            secret_key = os.getenv('MINIO_SECRET_KEY')
            self.__client = Minio(endpoint, access_key, secret_key, secure=False)

    def bucket_exists(self, bucket_name):
        """
        检查存储桶是否存在
        :param bucket_name: 存储桶名称
        :return: 如果存储桶存在返回 True，否则返回 False
        """
        try:
            return self.__client.bucket_exists(bucket_name)
        except S3Error as e:
            common.get_logger().error(f"Error checking bucket: {e}")
            return False

    def create_bucket(self, bucket_name):
        """
        创建存储桶
        :param bucket_name: 存储桶名称
        :return: 如果创建成功返回 True，否则返回 False
        """
        try:
            self.__client.make_bucket(bucket_name)
            return True
        except S3Error as e:
            common.get_logger().error(f"Error creating bucket: {e}")
            return False

    def remove_bucket(self, bucket_name):
        """
        删除存储桶
        :param bucket_name: 存储桶名称
        :return: 如果删除成功返回 True，否则返回 False
        """
        try:
            self.__client.remove_bucket(bucket_name)
            return True
        except S3Error as e:
            common.get_logger().error(f"Error removing bucket: {e}")
            return False

    def list_buckets(self):
        """
        列出所有存储桶
        :return: 存储桶列表
        """
        try:
            buckets = self.__client.list_buckets()
            return [bucket.name for bucket in buckets]
        except S3Error as e:
            common.get_logger().error(f"Error listing buckets: {e}")
            return []

    def upload_file(self, bucket_name, obj_name, file_obj, lenght, content_type='application/octet-stream'):
        """
        上传文件到存储桶
        :param bucket_name: 存储桶名称
        :param obj_name: 对象名称（在存储桶中的名称）
        :param file_obj: 文件对象
        :param lenght: 文件大小
        :param content_type: 文件类型
        :return: 如果上传成功返回 True，否则返回 False
        """
        try:
            if not self.bucket_exists(bucket_name):
                self.create_bucket(bucket_name)
            self.__client.put_object(bucket_name, obj_name, file_obj, lenght, content_type)
            return True
        except S3Error as e:
            common.get_logger().error(f"Error uploading file: {e}")
            return False

    def download_file(self, bucket_name, object_name, file_path):
        """
        从存储桶下载文件
        :param bucket_name: 存储桶名称
        :param object_name: 对象名称（在存储桶中的名称）
        :param file_path: 本地文件路径
        :return: 如果下载成功返回 True，否则返回 False
        """
        try:
            self.__client.fget_object(bucket_name, object_name, file_path)
            return True
        except S3Error as e:
            common.get_logger().error(f"Error downloading file: {e}")
            return False

    def delete_file(self, bucket_name, object_name):
        """
        从存储桶删除文件
        :param bucket_name: 存储桶名称
        :param object_name: 对象名称（在存储桶中的名称）
        :return: 如果删除成功返回 True，否则返回 False
        """
        try:
            self.__client.remove_object(bucket_name, object_name)
            return True
        except S3Error as e:
            common.get_logger().error(f"Error deleting file: {e}")
            return False

    def list_objects(self, bucket_name):
        """
        列出存储桶中的所有对象
        :param bucket_name: 存储桶名称
        :return: 对象列表
        """
        try:
            objects = self.__client.list_objects(bucket_name)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            common.get_logger().error(f"Error listing objects: {e}")
            return []
