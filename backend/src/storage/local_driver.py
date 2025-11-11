# backend/src/storage/local_driver.py
import os, shutil
from .driver import StorageDriver

class LocalDriver(StorageDriver):
    def __init__(self, base_path='./data'):
        self.base = base_path
        os.makedirs(self.base, exist_ok=True)
    def _full(self, key):
        return os.path.join(self.base, key)
    def create_presigned_upload(self, key: str, expires_in: int, content_type: str=None):
        # For local, return simple upload URL (POST to API) or instructions
        full = self._full(key)
        d = os.path.dirname(full)
        os.makedirs(d, exist_ok=True)
        return {'url': f'LOCAL://{full}', 'method':'LOCAL'}
    def upload(self, key: str, file_path: str) -> bool:
        dst = self._full(key)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(file_path, dst)
        return True
    def download(self, key: str, dest_path: str) -> bool:
        src = self._full(key)
        shutil.copyfile(src, dest_path)
        return True
    def delete(self, key: str) -> bool:
        try:
            os.remove(self._full(key))
            return True
        except Exception:
            return False
    def list(self, prefix: str) -> list:
        out = []
        root = os.path.join(self.base, prefix)
        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                out.append(os.path.relpath(os.path.join(dirpath,f), self.base))
        return out
