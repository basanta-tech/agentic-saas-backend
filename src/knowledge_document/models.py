from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class KnowledgeDocumentResponse(BaseModel):
  doc_id: int
  tenant_id: int
  title: Optional[str] = None
  source_type: Optional[str] = None
  source_url: Optional[str] = None
  content: Optional[str] = None
  created_at: datetime

  file_path: Optional[str] = None
  file_type: Optional[str] = None
  agent_ids: Optional[List[int]] = None

  model_config = {
    "from_attributes": True  
  }

class CreateKnowledgeDocumentRequest(BaseModel):
  title: Optional[str] = Field(None, max_length=255)
  source_type: Optional[str] = Field(None, max_length=50)
  source_url: Optional[str] = None
  content: Optional[str] = None