from datetime import datetime
from sqlalchemy import (
  Column,
  Integer,
  String,
  Text,
  DateTime,
  ForeignKey
)
from sqlalchemy.orm import relationship
from src.db.core import Base
from .association_tables import agent_document_association


class KnowledgeDocumentModel(Base):
  __tablename__ = "knowledge_documents"

  doc_id = Column(Integer, primary_key=True, autoincrement=True)
  tenant_id = Column(Integer, ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)

  title = Column(String(255))
  source_type = Column(String(50))
  source_url = Column(Text)
  content = Column(Text)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
  file_path = Column(String(500), nullable=True)
  file_type = Column(String(100), nullable=True)

  tenant = relationship("TenantModel", backref="knowledge_documents")

  agents = relationship(
    "AgentModel",
    secondary=agent_document_association,
    back_populates="documents"
  )
