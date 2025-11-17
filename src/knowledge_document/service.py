import os
from pathlib import Path
from typing import List
from uuid import uuid4
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from src.db.core import DbSession
from src.db.entities.AgentModel import AgentModel
from src.db.entities.TenantModel import TenantModel
from src.db.entities.KnowledgeDocumentModel import KnowledgeDocumentModel
from src.knowledge_document.models import CreateKnowledgeDocumentRequest, KnowledgeDocumentResponse


def list_documents(db: DbSession, tenant_id: int) -> List[KnowledgeDocumentResponse]:
  documents = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.tenant_id == tenant_id).all()

  return [KnowledgeDocumentResponse.model_validate(t) for t in documents]

UPLOAD_ROOT = Path(__file__).parent.parent.parent / "uploads"

async def create_document( tenant_id: int, payload, file: UploadFile | None, db):
  # Ensure tenant exists
  tenant = db.query(TenantModel).filter_by(tenant_id=tenant_id).first()
  if not tenant:
    raise HTTPException(status_code=404, detail="Tenant not found")

  file_path = None
  file_type = None

  print("UPLOAD_ROOT: ", UPLOAD_ROOT)
  
  if file:
    # Create tenant directory if not exists
    tenant_folder = os.path.join(UPLOAD_ROOT, f"tenant_{tenant_id}")
    print("Tenant folder location: ", tenant_folder)
    os.makedirs(tenant_folder, exist_ok=True)

    # Unique filename
    ext = __get_extension(file=file)
    unique_name = f"{uuid4()}.{ext}"

    # full path
    file_path = os.path.join(tenant_folder, unique_name)
    file_type = file.content_type

    # Save file locally
    with open(file_path, "wb") as buffer:
      buffer.write(await file.read())
    print(f"--- SUCCESSFULLY WROTE FILE: {file_path} ---")

  # Save record in DB
  new_doc = KnowledgeDocumentModel(
    tenant_id=tenant_id,
    title=payload.title,
    source_type=payload.source_type,
    source_url=payload.source_url,
    content=payload.content,
    file_path=file_path,
    file_type=file_type,
  )

  db.add(new_doc)
  db.commit()
  db.refresh(new_doc)

  return new_doc

def list_docs_for_agent(db: DbSession, agent_id: int) -> List[KnowledgeDocumentResponse]:
  agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
  if not agent:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Agent not found")
  return agent.documents

def assign_document(db: DbSession, agent_id: int, doc_id: int) -> JSONResponse:
  agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
  doc = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.doc_id == doc_id).first()

  if not agent or not doc:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent or Document not found")

  agent.documents.append(doc)
  db.commit()
  db.refresh(agent)
  return JSONResponse(content={"message": "Assigned successfully"})

def remove_document(db: DbSession, agent_id: int, doc_id: int) -> JSONResponse:
  agent = db.query(AgentModel).filter(AgentModel.agent_id == agent_id).first()
  doc = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.doc_id == doc_id).first()

  if not agent or not doc:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Agent or Document not found")

  agent.documents.remove(doc)
  db.commit()
  return JSONResponse(content={"message": "Removed successfully"})


def __get_extension(file):
  if not file or not file.filename:
    print("There is no filename")
    print(file.filename)
    return None
  return os.path.splitext(file.filename)[1].lstrip(".")