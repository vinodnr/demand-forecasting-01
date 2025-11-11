# backend/workers/convert_worker.py
import time, os, tempfile, shutil, traceback
from ..src.storage.local_driver import LocalDriver
from ..src.storage.minio_driver import MinIODriver
import pandas as pd

# This worker expects job dict: {'key': 'region/orgid/uuid/filename', 'org_id': '<uuid>', 'plan':'free'}
def process_job(job):
    try:
        key = job['key']
        org_id = job.get('org_id')
        plan = job.get('plan','free')
        # choose storage (local driver for dev)
        driver = LocalDriver(base_path=os.getenv('LOCAL_STORAGE_PATH','./data'))
        # download source to temp
        tmpdir = tempfile.mkdtemp()
        src = os.path.join(tmpdir, 'srcfile')
        driver.download(key, src)
        # try to read with pandas (supports xlsx, xls, csv)
        try:
            if key.lower().endswith('.csv'):
                df = pd.read_csv(src)
            else:
                df = pd.read_excel(src)
        except Exception as e:
            raise
        out_csv = os.path.join(tmpdir, 'converted.csv')
        df.to_csv(out_csv, index=False)
        # upload converted file next to original
        out_key = key + '.clean.csv'
        driver.upload(out_key, out_csv)
        # retention policy: if plan == 'free' delete original
        if plan == 'free':
            driver.delete(key)
        # write job audit (placeholder)
        print('Job processed for', key, 'out:', out_key)
        shutil.rmtree(tmpdir)
        return {'status':'ok', 'out_key': out_key}
    except Exception as e:
        traceback.print_exc()
        return {'status':'error', 'error': str(e)}
