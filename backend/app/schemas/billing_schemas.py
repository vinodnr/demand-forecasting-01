from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SubscribeIn(BaseModel):
    org_id: str
    plan_id: str

class ReportUsageIn(BaseModel):
    org_id: str
    metric: str
    value: float
    metadata: Optional[Dict[str, Any]] = None
