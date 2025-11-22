from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.db.core import DbSession, get_db
from src.db.entities.TenantModel import TenantModel
from src.db.entities.AgentModel import AgentModel
from . import service
from .models import AgentResponse, CreateAgentRequest
import os
import subprocess
from src.db.core import settings

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
  Fetches an agent's config from the DB and launches it as a new process.
  """
  
  agent = service.get_agent(db, tenant_id, agent_id)
  if not agent:
    raise HTTPException(status_code=404, detail="Agent not found")

  # 2. Get the current environment (which includes OPENAI_API_KEY from the server's .env)
  process_env = os.environ.copy()
  process_env["LIVEKIT_API_KEY"] = str(settings.LIVEKIT_API_KEY)
  process_env["LIVEKIT_API_SECRET"] = str(settings.LIVEKIT_API_SECRET)
  process_env["LIVEKIT_URL"] = str(settings.LIVEKIT_URL)
  process_env["NEXT_PUBLIC_LIVEKIT_URL"] = str(settings.NEXT_PUBLIC_LIVEKIT_URL)
  process_env["OPENAI_API_KEY"] = str(settings.OPENAI_API_KEY)
  process_env["AGENT_NAME"] = agent.name
  process_env["AGENT_ID"] = str(agent.agent_id)
  process_env["TENANT_ID"] = str(agent.tenant_id)

  # Define the command to run the agent
  # (This assumes your API server is run from the project root)
  command = [
    "uv", 
    "run", 
    "python", 
    "-m",
    "src.livekit-agent.agent",
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