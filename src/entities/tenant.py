from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime

class Tenant(BaseModel):
  __tablename__="tenants"
  
  tenant_id: UUID = Field(default_factory=uuid4, description="Unique tenant identifier")
  name: str = Field(..., max_length=255, description="Tenant name")
  domain: Optional[str] = Field(None, max_length=255, description="Tenant's domain name")
  plan: Optional[str] = Field(None, max_length=50, description="Subscription plan name")
  created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when tenant was created")