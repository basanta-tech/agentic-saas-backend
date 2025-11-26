from fastapi import APIRouter, HTTPException
from livekit import api
from src.db.core import settings, DbSession
from src.agent.service import get_agent_by_id
import os
import asyncio
import httpx

router = APIRouter(
  tags=["Health & Token"]
)

room_name="voice-agent-room"

@router.get("/health")
async def health_check() -> dict:
  """Simple liveness health check."""
  return {"status": "ok"}

async def create_explicit_dispatch(agent_name:str):
  lkapi = api.LiveKitAPI()

  dispatch = await lkapi.agent_dispatch.create_dispatch(
    api.CreateAgentDispatchRequest(
      agent_name=agent_name, room=room_name, metadata="my_metadata"
    )
  )
  print("created dispatch", dispatch)

  dispatches = await lkapi.agent_dispatch.list_dispatch(room_name=room_name)
  print(f"there are {len(dispatches)} dispatches in {room_name}")
  await lkapi.aclose()

\

@router.get("/token")
async def get_token(agent_id: int, db: DbSession) -> dict:
  """
  1. Triggers agent deployment via API.
  2. Waits 3 seconds for cold start.
  3. Generates LiveKit token and dispatches agent.
  """

  agent = get_agent_by_id(db, agent_id)
  if not agent:
    raise HTTPException(status_code=404, detail="Agent not found")
      
  agent_name = agent.name
  tenant_id = agent.tenant_id

  base_url = os.getenv("API_BASE_URL", "http://localhost:8000") 
  deploy_url = f"{base_url}/tenants/{tenant_id}/agents/{agent_id}/deploy"

  try:
      async with httpx.AsyncClient() as client:
        response = await client.post(deploy_url)
        
        if response.status_code not in [200, 201]:
          print(f"Warning: Deploy endpoint returned {response.status_code}")

  except Exception as e:
      print(f"Error calling deploy endpoint: {e}")


  print("Waiting for agent to warm up...")
  await asyncio.sleep(3)


  participant_identity = f"user-{os.urandom(4).hex()}"
  room_name = f"room-{agent_name}-{os.urandom(4).hex()}"


  token = api.AccessToken(
    settings.LIVEKIT_API_KEY,
    settings.LIVEKIT_API_SECRET,
  )
  token.with_identity(participant_identity)
  token.with_name(participant_identity)
  token.with_grants(
    api.VideoGrants(
      room_join=True,
      room=room_name,
      can_publish=True,
      can_subscribe=True,
    )
  )
  token.with_room_config(
      api.RoomConfiguration(
          agents=[
              api.RoomAgentDispatch(
                  agent_name=agent_name
              )
          ],
      ),
  )

  print(f"Creating explicit dispatch for agent: {agent_name} in room: {room_name}")
  
  await create_explicit_dispatch(agent_name) 

  return {"token": token.to_jwt(), "room_name": room_name}