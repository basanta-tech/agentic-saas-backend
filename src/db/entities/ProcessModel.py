from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.core import Base


class ProcessModel(Base):
  __tablename__ = "processes"

  process_id = Column(Integer, primary_key=True, autoincrement=True)
  agent_id = Column(Integer, ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
  pid = Column(Integer, nullable=False)         
  is_active = Column(Boolean, default=True, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

  agent = relationship("AgentModel", backref="processes")
