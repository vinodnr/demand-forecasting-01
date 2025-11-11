# backend/src/storage/driver.py
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
class StorageDriver(ABC):
    @abstractmethod
    def create_presigned_upload(self, key: str, expires_in: int, content_type: str=None) -> Dict[str,Any]:
        raise NotImplementedError()
    @abstractmethod
    def upload(self, key: str, file_path: str) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def download(self, key: str, dest_path: str) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError()
    @abstractmethod
    def list(self, prefix: str) -> list:
        raise NotImplementedError()
