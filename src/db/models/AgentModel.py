import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Enum as SqlEnum,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.core import Base


class LanguageEnum(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    JAPANESE = "ja"
    CHINESE = "zh"
    ARABIC = "ar"


class AgentModel(Base):
    __tablename__ = "agents"

    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    language = Column(SqlEnum(LanguageEnum), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # optional relationship (if you have Tenant model)
    tenant = relationship("TenantModel", backref="agents")
