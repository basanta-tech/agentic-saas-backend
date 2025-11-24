import os
from fastapi import APIRouter
from livekit import api
from src.db.core import settings

router = APIRouter(
  tags=["Health & Token"]
)

ROOM_NAME = "voice-agent-room"

@router.get("/health")
async def health_check() -> dict:
  """Simple liveness health check."""
  return {"status": "ok"}


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
      room=ROOM_NAME,
      can_publish=True,
      can_subscribe=True,
    )
  )

  return {"token": token.to_jwt()}
