from fastapi import FastAPI
from src.tenant.controller import router as tenant_router

def register_routes(app: FastAPI):
  app.include_router(tenant_router)