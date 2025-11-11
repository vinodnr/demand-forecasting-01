# backend/tests/test_presign_quota.py
import os, requests, json
# This is an integration-style test expecting a running dev compose (postgres+backend)
BASE = os.getenv('BASE_URL','http://localhost:8000')
def test_presign_requires_org_header():
    r = requests.post(BASE + '/v1/storage/presign', json={'filename':'a.csv','size':10})
    assert r.status_code == 400 or r.status_code == 401
