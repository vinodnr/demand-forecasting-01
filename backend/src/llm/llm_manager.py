# backend/src/llm/llm_manager.py
# small wrapper to reuse existing llm_manager service; placeholder to centralize interfaces
from ..services import llm_manager as service

def get_provider_for_org(org_id=None, plan_id=None):
    return service.get_provider_for_org(org_id=org_id, plan_id=plan_id)
