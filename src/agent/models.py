from datetime import datetime
from pydantic import BaseModel, Field
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

class CreateAgentRequest(BaseModel):
  name: str = Field(..., min_length=1, max_length=255)
  description: Optional[str] = Field(None, max_length=1000)
  language: LanguageEnum = Field(...)
  is_active: bool = True

