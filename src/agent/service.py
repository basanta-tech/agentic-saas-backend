from typing import List
from fastapi import Depends, HTTPException
from src.agent.models import AgentResponse
from src.db.core import DbSession, get_db
from src.db.entities.TenantModel import TenantModel
from src.db.entities.AgentModel import AgentModel


def list_agents(tenant_id: int, db: DbSession) -> List[AgentResponse]:
  agents = db.query(AgentModel).filter(AgentModel.tenant_id == tenant_id).all()
  return [AgentResponse.model_validate(t) for t in agents]

def create_agent(db: DbSession, tenant_id: int, payload) -> AgentResponse:
  # Ensure tenant exists
  tenant_exists = db.query(TenantModel).filter(TenantModel.tenant_id == tenant_id).first()
  if not tenant_exists:
    raise HTTPException(status_code=404, detail="Tenant not found")

  agent = AgentModel(
    tenant_id=tenant_id,
    **payload.model_dump()
  )
  db.add(agent)
  db.commit()
  db.refresh(agent)
  return agent