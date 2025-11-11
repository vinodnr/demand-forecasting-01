# backend/src/api/presign.py
from fastapi import APIRouter, HTTPException, Depends, Request
from ..storage.local_driver import LocalDriver
from ..storage.minio_driver import MinIODriver
import os, uuid
router = APIRouter(prefix='/v1/storage', tags=['storage'])

def get_driver_for_org(org_region='us'):
    mode = os.getenv('STORAGE_MODE', 'local')
    if mode == 'minio':
        bucket = os.getenv(f'MINIO_BUCKET_{org_region.upper()}', os.getenv('MINIO_BUCKET','dev'))
        return MinIODriver(bucket=bucket)
    else:
        base = os.getenv('LOCAL_STORAGE_PATH','./data')
        return LocalDriver(base_path=base)

@router.post('/presign')
async def presign_upload(request: Request):
    body = await request.json()
    filename = body.get('filename')
    size = int(body.get('size', 0))
    org_region = request.headers.get('x-region','us')
    if not filename:
        raise HTTPException(400, 'filename required')
    # enforcement: simple size limit per tier (TODO: replace with DB lookup)
    MAX_FREE = int(os.getenv('MAX_FREE_UPLOAD_BYTES','104857600')) #100MB
    # choose driver per region
    driver = get_driver_for_org(org_region)
    key = f"{org_region}/{uuid.uuid4().hex}/{filename}"
    # if local, return special instruction
    pres = driver.create_presigned_upload(key, expires_in=3600, content_type=body.get('content_type'))
    return {'key': key, 'presign': pres}

# quota-enforced presign endpoint
from ..middleware.quotas import storage_quota_dependency
@router.post('/presign-enforced')
async def presign_upload_enforced(request: Request, _check=Depends(storage_quota_dependency)):
    # re-use presign logic
    return await presign_upload(request)
