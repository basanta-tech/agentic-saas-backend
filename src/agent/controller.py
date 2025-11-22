from typing import List
from fastapi import APIRouter, HTTPException, status
from src.db.core import DbSession
from . import service
from src.tenant.service import get_tenant_by_id
from .models import AgentResponse, CreateAgentRequest
import os
import subprocess

router = APIRouter(
  prefix="/tenants/{tenant_id}/agents",
  tags=["Agents"]
)

# GET all agents for a tenant
@router.get("/", response_model=List[AgentResponse])
def list_agents(tenant_id: int, db: DbSession):
  return service.list_agents(tenant_id, db)


# POST: create agent under tenant
@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(tenant_id: int, payload: CreateAgentRequest, db: DbSession):
  return service.create_agent(db, tenant_id, payload)

# GET: single agent
@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(tenant_id: int, agent_id: int, db: DbSession):
  return service.get_agent(db, tenant_id, agent_id)

@router.post(
  "/{agent_id}/deploy", 
  status_code=status.HTTP_202_ACCEPTED, 
  response_model=dict
)
def deploy_agent(tenant_id: int, agent_id: int, db: DbSession):
  """
  Fetches an agent's, tenant's config from the DB and launches it as a new process.
  """
  tenant = get_tenant_by_id(db, tenant_id)
  if not tenant:
    raise HTTPException(status_code=404, detail="Tenant not found")
  
  agent = service.get_agent(db, tenant_id, agent_id)
  if not agent:
    raise HTTPException(status_code=404, detail="Agent not found")

  # 2. Get the current environment variables
  process_env = os.environ.copy()
  process_env["AGENT_NAME"] = str(agent.name)
  process_env["TENANT_ID"] = str(agent.tenant_id)
  process_env["LANG_CODE"] = str(agent.language)
  process_env["TENANT_NAME"] = str(tenant.name)
  print("LANG_CODE: ",str(agent.language))

  # Define the command to run the agent
  # (This assumes your API server is run from the project root)
  command = [
    "uv", 
    "run", 
    "python", 
    "-m",
    "src.livekit_agent.agent",
    "dev"
  ]

  # Launch the agent in a new, non-blocking process
  try:
    process = subprocess.Popen(command, env=process_env)
    
    # Return an immediate "accepted" response
    return {
      "status": "deploy_initiated", 
      "agent_id": agent.agent_id, 
      "pid": process.pid 
    }
  except Exception as e:
    
    raise HTTPException(
      status_code=500, 
      detail=f"Failed to launch agent process: {e}"
    )