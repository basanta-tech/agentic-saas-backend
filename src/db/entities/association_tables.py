from sqlalchemy import Table, Column, Integer, ForeignKey
from src.db.core import Base

agent_document_association = Table(
  "agent_documents",
  Base.metadata,
  Column("agent_id", Integer, ForeignKey("agents.agent_id", ondelete="CASCADE"), primary_key=True),
  Column("doc_id", Integer, ForeignKey("knowledge_documents.doc_id", ondelete="CASCADE"), primary_key=True),
)
