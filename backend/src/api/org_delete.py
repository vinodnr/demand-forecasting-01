# backend/src/api/org_delete.py
from fastapi import APIRouter, Body, Depends, HTTPException
from ..services.llm_manager import register_db_get_conn
from ..workers.jobs import enqueue
router = APIRouter(prefix='/v1/org', tags=['org'])

@router.post('/request-delete')
def request_delete(body: dict = Body(...)):
    org_id = body.get('org_id')
    reason = body.get('reason', 'requested by owner')
    owner_id = body.get('owner_id')
    if not org_id or not owner_id:
        raise HTTPException(400, 'org_id and owner_id required')
    # create deletion job and enqueue
    job = {'type':'delete_org','org_id':org_id,'reason':reason,'owner_id':owner_id}
    enqueue(job)
    return {'status':'enqueued'}
