from typing import List
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from src.db.core import DbSession
from src.db.entities.AgentModel import AgentModel
from src.db.entities.TenantModel import TenantModel
from src.db.entities.KnowledgeDocumentModel import KnowledgeDocumentModel
from src.knowledge_document.models import CreateKnowledgeDocumentRequest, KnowledgeDocumentResponse


def list_documents(db: DbSession, tenant_id: int) -> List[KnowledgeDocumentResponse]:
  documents = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.tenant_id == tenant_id).all()

  return [KnowledgeDocumentResponse.model_validate(t) for t in documents]

def create_document(db: DbSession, tenant_id: int, payload: CreateKnowledgeDocumentRequest) -> KnowledgeDocumentResponse:
  # Ensure tenant exists
  tenant = db.query(TenantModel).filter(TenantModel.tenant_id == tenant_id).first()
  if not tenant:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Tenant not found"
    )

  new_doc = KnowledgeDocumentModel(
    tenant_id=tenant_id,
    title=payload.title,
    source_type=payload.source_type,
    source_url=payload.source_url,
    content=payload.content,
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