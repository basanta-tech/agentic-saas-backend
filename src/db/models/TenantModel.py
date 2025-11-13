from sqlalchemy import Column, String, DateTime
from sqlalchemy import (UUID)
from datetime import datetime
import uuid
from src.db.core import Base

class TenantModel(Base):
  __tablename__ = "tenants"

  tenant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String(255), nullable=False)
  domain = Column(String(255), nullable=True)
  plan = Column(String(50), nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)
