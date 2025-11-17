from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.db.entities.AgentModel import LanguageEnum



class AgentResponse(BaseModel):
  agent_id: int
  tenant_id: int
  name: str
  description: Optional[str] = None
  language: LanguageEnum
  is_active: bool
  created_at: datetime

  model_config = {
    "from_attributes": True
  }


