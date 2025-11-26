import os
from fastapi import APIRouter
from livekit import api
from src.db.core import settings

router = APIRouter(
  tags=["Health & Token"]
)

agent_name="finance-agent"
room_name="voice-agent-room"

@router.get("/health")
async def health_check() -> dict:
  """Simple liveness health check."""
  return {"status": "ok"}

async def create_explicit_dispatch():
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

@router.get("/token")
async def get_token() -> dict:
  """
  Generate a LiveKit access token for a randomly identified participant.
  """
  participant_identity = f"user-{os.urandom(4).hex()}"

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
          agent_name="finance-agent"
        )
      ],
    ),
  )
  print("creating explicit dispatch")
  await create_explicit_dispatch()
  return {"token": token.to_jwt()}