from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class LanguageEnum(str, Enum):
  ENGLISH = "en"
  HINDI = "hi"
  SPANISH = "es"
  FRENCH = "fr"
  GERMAN = "de"
  JAPANESE = "ja"
  CHINESE = "zh"
  ARABIC = "ar"

class Agent(BaseModel):
  __tablename__="agents"
  
  agent_id: UUID = Field(default_factory=uuid4, description="Unique agent identifier")
  tenant_id: UUID = Field(..., description="Foreign key to tenants table")
  name: str = Field(..., max_length=255, description="Agent's name")
  description: Optional[str] = Field(None, description="Agent description or purpose")
  language: LanguageEnum = Field(..., description="Agent's preferred language (must match predefined list)")
  is_active: bool = Field(default=True, description="Is the agent active?")
  created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")