from typing import List
from fastapi import APIRouter, Depends, status
from src.db.core import DbSession
from .models import CreateKnowledgeDocumentRequest, KnowledgeDocumentResponse
from . import service

router = APIRouter(
  prefix="/tenants/{tenant_id}/documents",
  tags=["Knowledge Documents"]
)

@router.get("/", response_model=List[KnowledgeDocumentResponse])
def list_documents(tenant_id: int, db: DbSession):
  return service.list_documents(db, tenant_id)


@router.post("/", response_model=KnowledgeDocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(tenant_id: int, payload: CreateKnowledgeDocumentRequest, db: DbSession):
  return service.create_document(db, tenant_id, payload)