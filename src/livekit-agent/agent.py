from dotenv import load_dotenv
from pathlib import Path
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from llama_index.core import (
  SimpleDirectoryReader,
  StorageContext,
  VectorStoreIndex,
  load_index_from_storage,
)
import os

load_dotenv(".env")

# check if storage already exists
THIS_DIR = Path(__file__).parent
UPLOAD_DIR = THIS_DIR.parent.parent
PERSIST_DIR = THIS_DIR / "query-engine-storage"
if not PERSIST_DIR.exists():
  # load the documents and create the index
  documents = SimpleDirectoryReader(UPLOAD_DIR / "uploads/tenant_2").load_data()
  index = VectorStoreIndex.from_documents(documents)
  # store it for later
  index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
  # load the existing index
  storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR) # type: ignore
  index = load_index_from_storage(storage_context)

@function_tool()
async def query_info(query: str) -> str:
  """Get more information about a specific topic"""
  query_engine = index.as_query_engine(use_async=True)
  res = await query_engine.aquery(query)
  print("Query result:", res)
  return str(res)

class Assistant(Agent):
  def __init__(self) -> None:
    super().__init__(
      instructions="""You are a helpful voice AI assistant.
      You eagerly assist users with their questions by providing information from your extensive knowledge.
      Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
      You are curious, friendly, and have a sense of humor.""",
      tools=[query_info]
    )

async def entrypoint(ctx: agents.JobContext):
  session = AgentSession(
    stt="assemblyai/universal-streaming:en",
    llm="openai/gpt-4.1-mini",
    tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    vad=silero.VAD.load(),
    turn_detection=MultilingualModel(),
  )

  await session.start(
    room=ctx.room,
    agent=Assistant(),
    room_input_options=RoomInputOptions(
      # For telephony applications, use `BVCTelephony` instead for best results
      noise_cancellation=noise_cancellation.BVC(), 
    ),
  )

  await session.generate_reply(
    instructions="Greet the user and offer your assistance."
  )


if __name__ == "__main__":
  agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))