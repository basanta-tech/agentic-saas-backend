from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import UTC, datetime
from src.db.core import Base

class TenantModel(Base):
  __tablename__ = "tenants"

  tenant_id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  domain = Column(String(255), nullable=True)
  plan = Column(String(50), nullable=True)
  is_active = Column(Boolean, default=True, nullable=False)
  created_at = Column(DateTime, default=lambda:datetime.now(UTC))
