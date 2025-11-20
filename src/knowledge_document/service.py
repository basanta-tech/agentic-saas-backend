import os
from pathlib import Path
from typing import List
from uuid import uuid4
from aiohttp import ClientError
import boto3
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from src.db.core import DbSession
from src.db.entities.AgentModel import AgentModel
from src.db.entities.TenantModel import TenantModel
from src.db.entities.KnowledgeDocumentModel import KnowledgeDocumentModel
from src.knowledge_document.models import CreateKnowledgeDocumentRequest, KnowledgeDocumentResponse
from src.db.core import settings
from dotenv import load_dotenv
load_dotenv()
from src.db.core import settings


def list_documents(db: DbSession, tenant_id: int) -> List[KnowledgeDocumentResponse]:
  documents = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.tenant_id == tenant_id).all()

  return [KnowledgeDocumentResponse.model_validate(t) for t in documents]

async def create_document(tenant_id: int, payload, file: UploadFile | None, db):
  # Ensure tenant exists (No change here)
  tenant = db.query(TenantModel).filter_by(tenant_id=tenant_id).first()
  if not tenant:
    raise HTTPException(status_code=404, detail="Tenant not found")

  file_path = None
  file_type = None

  if file:
    ext = __get_extension(file=file)
    unique_name = f"{uuid4()}.{ext}"
    
    # We use a folder structure in S3 for organization, e.g., 'tenant_1/unique_id.ext'
    s3_key = f"tenant_{tenant_id}/{unique_name}"
    file_type = file.content_type

    # We need to read the whole file content into the memory to pass to S3's put_object
    file_content = await file.read()
    
    try:
      # 3. Upload to S3
      settings.s3_client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=s3_key,
        Body=file_content,
        ContentType=file_type
      )
      print(f"--- SUCCESSFULLY WROTE FILE TO S3: s3://{settings.S3_BUCKET_NAME}/{s3_key} ---")
      
      # Save the S3 Key (Path) to the DB
      # This is the reference we'll use to retrieve the file later
      file_path = s3_key 

    except ClientError as e:
      print(f"S3 Upload Failed: {e}")
      raise HTTPException(status_code=500, detail="Could not upload file to cloud storage.")
    except Exception as e:
      print(f"An unexpected error occurred: {e}")
      raise HTTPException(status_code=500, detail="An unexpected error occurred during file upload.")


  # Save record in DB (Minimal change, we use s3_key as file_path)
  new_doc = KnowledgeDocumentModel(
    tenant_id=tenant_id,
    title=payload.title,
    source_type=payload.source_type,
    source_url=payload.source_url,
    content=payload.content,
    file_path=file_path, # This now stores the S3 Key
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


def __get_extension(file: UploadFile) -> str:
  if file.filename:
    return file.filename.split('.')[-1]
  return "bin" 