import os
import shutil
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
  __remove_query_engine_storage(tenant_id)
  payload_data = json.loads(payload)
  payload_model = CreateKnowledgeDocumentRequest(**payload_data)

  return await service.create_document(tenant_id, payload_model, file, db)


@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
async def delete_document(
  tenant_id: int,
  document_id: int,
  db: DbSession
):
  __remove_query_engine_storage(tenant_id)
  return await service.delete_document(db, tenant_id, document_id)


@router.get("/{document_id}/download")
async def download_document(
  tenant_id: int,
  document_id: int,
  db: DbSession
):
  return await service.download_document(db, tenant_id, document_id)


def __remove_query_engine_storage(tenant_id):
  # Get the directory of the current file (src/knowledge_document)
  current_dir = os.path.dirname(os.path.abspath(__file__))
  # Navigate up to src and then to livekit_agent
  folder_path = os.path.join(current_dir, "..", "livekit_agent", "query-engine-storage", f"tenant_{tenant_id}")
  folder_path = os.path.normpath(folder_path)
  
  print("Folder Path: ", folder_path)
  if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
    print("Folder deleted!")
  else:
    print("Folder does not exist.")