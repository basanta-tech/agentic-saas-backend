from dotenv import load_dotenv
from pathlib import Path
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool
from livekit.plugins import (noise_cancellation, silero, google)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from llama_index.core import (
  SimpleDirectoryReader,
  StorageContext,
  VectorStoreIndex,
  load_index_from_storage,
)
from google.genai import types

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
  """Retrieve factual information from the uploaded knowledge documents.

  Use this tool ONLY to look up information that may be present in the knowledge base.

  When calling this tool:
  - Rewrite the user’s question into a short, precise search query.
  - Remove conversational phrasing or unnecessary words.
  - Include only keywords and concepts relevant to the topic.
  - Do NOT pass long sentences or full user questions.
  - Keep the query minimal but highly descriptive.

  This tool returns relevant text chunks from the knowledge base. Always wait for the tool response before answering the user."""

  query_engine = index.as_query_engine(use_async=True)
  res = await query_engine.aquery(query)
  print("Query result:", res)
  return str(res)

class Assistant(Agent):
  def __init__(self) -> None:
    super().__init__(
      instructions="""
        You speak in Hindi by default and must give all responses in Hindi unless the user speaks in another language.  
        If the user switches to a different language, reply in that same language.  
        You maintain a male persona and use he/him pronouns whenever referring to yourself.

        Your job is to answer user questions accurately using information from the provided knowledge sources. Follow this process:

        1. First, examine the user's query carefully.

        2. Decide whether the answer may exist in the uploaded documents.
          - If yes, call the query_info tool using a clean, concise search query.
          - If not, answer directly without calling the tool.

        3. You MUST call query_info when:
          - The user requests factual, technical, or specific information.
          - The question likely depends on stored knowledge, documentation, or internal details.
          - The question cannot be reliably answered from general reasoning alone.

        4. DO NOT call query_info when:
          - The user is greeting, chatting, or making small talk.
          - The user asks a subjective question not dependent on the documents.
          - You already have enough information to answer without retrieval.

        5. When creating the tool query:
          - Rewrite the user’s question into a short, precise search prompt.
          - Remove unnecessary words or conversation style.
          - Only include information useful for retrieval.

        6. After you receive the tool result:
          - Read the retrieved context carefully.
          - Use it to craft a clear and concise answer.
          - If the context is insufficient or irrelevant, answer to the best of your ability and state that the document did not explicitly cover the topic.

        7. Never hallucinate details that are not present in the retrieved context or your allowed knowledge.

        Your final answer must be simple, clear, and free of special formatting, symbols, or emojis.
      """,
      tools=[query_info]
    )

async def entrypoint(ctx: agents.JobContext):
  session = AgentSession(
    llm=google.realtime.RealtimeModel(),
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