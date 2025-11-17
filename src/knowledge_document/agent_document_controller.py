from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.db.core import DbSession
from .models import CreateKnowledgeDocumentRequest, KnowledgeDocumentResponse
from . import service

router = APIRouter(
  prefix="/agents/{agent_id}/documents",
  tags=["Knowledge Documents"]
)

@router.get("/")
def list_docs_for_agent(agent_id: int, db: DbSession) -> List[KnowledgeDocumentResponse]:
  return service.list_docs_for_agent(db, agent_id)

@router.post("/{doc_id}", status_code=status.HTTP_201_CREATED)
def assign_doc(agent_id: int, doc_id: int, db: DbSession) -> JSONResponse:
  return service.assign_document(db, agent_id, doc_id)

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_doc(agent_id: int, doc_id: int, db: DbSession) -> JSONResponse:
  return service.remove_document(db, agent_id, doc_id)