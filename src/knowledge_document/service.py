from typing import List

from fastapi import HTTPException, status
from src.db.core import DbSession
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
