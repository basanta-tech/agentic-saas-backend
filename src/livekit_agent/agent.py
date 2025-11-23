import os
from typing import List
from dotenv import load_dotenv
from pathlib import Path
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool
from livekit.plugins import (noise_cancellation, silero, google, openai, sarvam)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
import s3fs
from src.db.core import settings
from llama_index.core import (
  SimpleDirectoryReader,
  StorageContext,
  VectorStoreIndex,
  load_index_from_storage,
  Document
)
from google.genai import types

load_dotenv(".env")
TENANT_ID = os.getenv("TENANT_ID",1)
AGENT_NAME = os.getenv("AGENT_NAME")
LANG_CODE = str(os.getenv("LANG_CODE"))
print("LANG_CODE: ",LANG_CODE)
TENANT_NAME = str(os.getenv("TENANT_NAME"))
print("TENANT_NAME: ",TENANT_NAME)

S3_BUCKET_NAME = settings.S3_BUCKET_NAME
S3_INPUT_DIR = f"{S3_BUCKET_NAME}/tenant_{TENANT_ID}/uploads/"

# --- S3 File System Setup ---
# Create an S3FileSystem instance using credentials from settings
s3_fs = s3fs.S3FileSystem(
  key=settings.AWS_ACCESS_KEY_ID,
  secret=settings.AWS_SECRET_ACCESS_KEY,
  client_kwargs={'region_name': settings.AWS_DEFAULT_REGION}
)

# --- Document Loading Function ---
def load_documents_from_s3() -> List[Document]:
  """Loads documents from S3 using SimpleDirectoryReader with an s3fs filesystem."""
  
  print(f"Loading documents from S3 path: s3://{S3_INPUT_DIR}")
  
  # Initialize the SimpleDirectoryReader
  loader = SimpleDirectoryReader(
    input_dir=S3_INPUT_DIR, # The S3 path
    fs=s3_fs,               # <-- Pass the configured s3fs instance here
  )
  
  return loader.load_data()

# check if storage already exists
THIS_DIR = Path(__file__).parent
PERSIST_DIR = THIS_DIR / "query-engine-storage" / f"tenant_{TENANT_ID}"

if not PERSIST_DIR.exists():
  print("Storage not found. Creating index from S3 documents...")

 # Call the new S3 loading function
  documents = load_documents_from_s3()

  if not documents:
    print("Warning: No documents found in S3. Index will be empty.")

  index = VectorStoreIndex.from_documents(documents)
  # store it for later
  index.storage_context.persist(persist_dir=PERSIST_DIR)
  print(f"Index created and persisted to {PERSIST_DIR}")
else:
 # load the existing index
  print("Loading existing index from storage...")
  storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR) # type: ignore
  index = load_index_from_storage(storage_context)
  print("Index loaded.")

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
      instructions=f"""
        You are a female AI assistant(anushka) with access to a retrieval tool called query_info.
        You must respond **exclusively in the language specified by {LANG_CODE}**.
        All responses, tool queries, and internal reasoning must use only {LANG_CODE}.

        Follow this process:

        1. Examine the user's query carefully.

        2. Determine whether the answer may exist in the uploaded documents.
          - If yes, call the query_info tool using a short, precise search query written in {LANG_CODE}.
          - If not, answer directly in {LANG_CODE} without calling the tool.

        3. You MUST call query_info when:
          - The user asks for factual, technical, or specific information.
          - The question likely depends on stored knowledge, documentation, or internal details.
          - The answer cannot be reliably produced from general reasoning alone.

        4. DO NOT call query_info when:
          - The user is greeting, chatting, or making small talk.
          - The question is subjective or not based on documentation.
          - You already have enough information to answer confidently.

        5. When creating a tool query:
          - Rewrite the user’s question into a concise, keyword-focused search prompt.
          - Remove polite wording, conversational filler, and unnecessary details.
          - Use only terms useful for retrieval.
          - The query must be written entirely in {LANG_CODE}.

        6. After receiving the tool result:
          - Read the retrieved context carefully.
          - Use it to create a clear, concise answer in {LANG_CODE}.
          - If the documents do not explicitly cover the topic, answer in {LANG_CODE} and state that the information was not found.

        7. Never invent or hallucinate information not supported by the retrieved context or your allowed knowledge.

        8. Your final answer must always be simple, direct, written only in {LANG_CODE}, and free of special symbols, emojis, or unusual formatting.

      """,
      tools=[query_info]
    )

async def entrypoint(ctx: agents.JobContext):
  session = AgentSession(
    stt=sarvam.STT(
      language=LANG_CODE,
      model="saarika:v2.5",
    ),
    llm=openai.LLM(
        model="gpt-4o-mini"
    ),
    tts=sarvam.TTS(
      target_language_code=LANG_CODE,
      speaker="anushka",
      pace=1.05,
      enable_preprocessing=True
    ),
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
    instructions=f"""
     Greet the user warmly in {LANG_CODE} on behalf of **{TENANT_NAME}**.
      Introduce yourself as Anushka, a female assistant.
      State that you are ready to answer questions based on **{TENANT_NAME}'s** uploaded documents.
      Ensure you use feminine grammatical gender (e.g., 'sakti hoon') for yourself.
    """
  )


if __name__ == "__main__":
  agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))