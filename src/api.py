from fastapi import FastAPI
from src.tenant.controller import router as tenant_router
from src.agent.controller import router as agent_router
from src.knowledge_document.document_controller import router as knowledge_document_router
from src.knowledge_document.agent_document_controller import router as agent_docuemnt_router

def register_routes(app: FastAPI):
  app.include_router(tenant_router)
  app.include_router(agent_router)
  app.include_router(knowledge_document_router)
  app.include_router(agent_docuemnt_router)
