from typing import List
from fastapi import APIRouter, status
from ..db.core import DbSession
from .models import TenantResponse, CreateTenantRequest
from . import service
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/tenants",
  tags=["Tenants"]
)

@router.get("/", response_model=List[TenantResponse])
def get_tenants(db: DbSession):
  return service.get_all_tenants(db)


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: CreateTenantRequest, db: DbSession):
  return service.create_tenant(db, payload)

