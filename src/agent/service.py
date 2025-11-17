from typing import List
from fastapi import Depends
from src.agent.models import AgentResponse
from src.db.core import DbSession, get_db
from src.db.entities.AgentModel import AgentModel


def list_agents(tenant_id: int, db: DbSession) -> List[AgentResponse]:
  agents = db.query(AgentModel).filter(AgentModel.tenant_id == tenant_id).all()
  return [AgentResponse.model_validate(t) for t in agents]