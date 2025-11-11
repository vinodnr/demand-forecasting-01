# backend/src/storage/minio_driver.py
import os, json, time
from minio import Minio
from urllib.parse import urljoin
from .driver import StorageDriver

class MinIODriver(StorageDriver):
    def __init__(self, bucket, endpoint=None, access_key=None, secret_key=None, secure=True):
        endpoint = endpoint or os.getenv('MINIO_ENDPOINT', 'localhost:9000')
        access_key = access_key or os.getenv('MINIO_ACCESS_KEY')
        secret_key = secret_key or os.getenv('MINIO_SECRET_KEY')
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.bucket = bucket
        # ensure bucket
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)
    def create_presigned_upload(self, key: str, expires_in: int, content_type: str=None):
        # MinIO presigned PUT
        url = self.client.presigned_put_object(self.bucket, key, expires=int(expires_in))
        return {'url': url, 'method': 'PUT'}
    def upload(self, key: str, file_path: str) -> bool:
        self.client.fput_object(self.bucket, key, file_path)
        return True
    def download(self, key: str, dest_path: str) -> bool:
        self.client.fget_object(self.bucket, key, dest_path)
        return True
    def delete(self, key: str) -> bool:
        self.client.remove_object(self.bucket, key)
        return True
    def list(self, prefix: str) -> list:
        return [obj.object_name for obj in self.client.list_objects(self.bucket, prefix=prefix, recursive=True)]
