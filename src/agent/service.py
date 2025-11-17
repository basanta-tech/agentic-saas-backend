from typing import List
from fastapi import Depends, HTTPException, status
from src.agent.models import AgentResponse
from src.db.core import DbSession, get_db
from src.db.entities.TenantModel import TenantModel
from src.db.entities.AgentModel import AgentModel


def list_agents(tenant_id: int, db: DbSession) -> List[AgentResponse]:
  # Ensure tenant exists
  tenant_exists = db.query(TenantModel).filter(TenantModel.tenant_id == tenant_id).first()
  if not tenant_exists:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
  
  agents = db.query(AgentModel).filter(AgentModel.tenant_id == tenant_id).all()
  return [AgentResponse.model_validate(t) for t in agents]

def create_agent(db: DbSession, tenant_id: int, payload) -> AgentResponse:
  # Ensure tenant exists
  tenant_exists = db.query(TenantModel).filter(TenantModel.tenant_id == tenant_id).first()
  if not tenant_exists:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

  agent = AgentModel(
    tenant_id=tenant_id,
    **payload.model_dump()
  )
  db.add(agent)
  db.commit()
  db.refresh(agent)
  return agent

def get_agent(db: DbSession, tenant_id: int, agent_id: int) -> AgentResponse:
  agent = (
    db.query(AgentModel)
    .filter(
      AgentModel.tenant_id == tenant_id,
      AgentModel.agent_id == agent_id
    )
    .first()
  )
  if not agent:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
  return agent