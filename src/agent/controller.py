from typing import List
from fastapi import APIRouter, Depends, HTTPException

from src.db.core import DbSession, get_db
from src.db.entities.TenantModel import TenantModel
from src.db.entities.AgentModel import AgentModel
from . import service
from .models import AgentResponse

router = APIRouter(
  prefix="/tenants/{tenant_id}/agents",
  tags=["Agents"]
)

# GET all agents for a tenant
@router.get("/", response_model=List[AgentResponse])
def list_agents(tenant_id: int, db: DbSession):
  return service.list_agents(tenant_id, db)
