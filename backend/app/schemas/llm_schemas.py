from pydantic import BaseModel
from typing import Optional, Dict, Any
class ProviderIn(BaseModel):
    provider_key: str
    display_name: str
    config: Optional[Dict[str, Any]] = {}
