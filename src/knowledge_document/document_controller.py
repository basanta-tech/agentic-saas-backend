from typing import Annotated, List
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from src.db.core import DbSession
from .models import CreateKnowledgeDocumentRequest, KnowledgeDocumentResponse
from . import service
import json

router = APIRouter(
  prefix="/tenants/{tenant_id}/documents",
  tags=["Knowledge Documents"]
)

@router.get("/", response_model=List[KnowledgeDocumentResponse])
def list_documents(tenant_id: int, db: DbSession):
  return service.list_documents(db, tenant_id)


@router.post("/", response_model=KnowledgeDocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
  tenant_id: int,  
  payload: Annotated[str, Form(...)],
  file: Annotated[UploadFile | None, File()],
  db: DbSession
):
  # Convert JSON string to Pydantic model
  payload_data = json.loads(payload)
  payload_model = CreateKnowledgeDocumentRequest(**payload_data)

  return await service.create_document(tenant_id, payload_model, file, db)
