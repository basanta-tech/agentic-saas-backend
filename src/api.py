from fastapi import FastAPI
from src.tenant.controller import router as tenant_router
from src.agent.controller import router as agent_router

def register_routes(app: FastAPI):
  app.include_router(tenant_router)
  app.include_router(agent_router)