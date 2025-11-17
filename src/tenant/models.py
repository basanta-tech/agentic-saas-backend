from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class TenantResponse(BaseModel):
  tenant_id: int
  name: str
  domain: str | None = None
  plan: str | None = None
  created_at: datetime

  model_config = {
    "from_attributes": True
  }

class CreateTenantRequest(BaseModel):
  name: str = Field(..., min_length=1, max_length=255)
  domain: str | None = Field(None, max_length=255)
  plan: str | None = Field(None, max_length=50)


class UpdateTenantRequest(BaseModel):
  name: str | None = Field(None, max_length=255)
  domain: str | None = Field(None, max_length=255)
  plan: str | None = Field(None, max_length=50)

