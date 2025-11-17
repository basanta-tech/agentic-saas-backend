from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Enum as SqlEnum,
    ForeignKey,
    UUID
)

from sqlalchemy.orm import relationship
from src.db.core import Base
from .association_tables import agent_document_association


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

    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    language = Column(SqlEnum(LanguageEnum), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tenant = relationship("TenantModel", backref="agents")

    documents = relationship(
        "KnowledgeDocumentModel",
        secondary=agent_document_association,
        back_populates="agents"
    )