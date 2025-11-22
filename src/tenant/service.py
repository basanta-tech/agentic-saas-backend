from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.entities.TenantModel import TenantModel
from .models import TenantResponse, CreateTenantRequest
from fastapi import status

def get_all_tenants(db: Session) -> List[TenantResponse]:
  tenants = db.query(TenantModel).all()
  return [TenantResponse.model_validate(t) for t in tenants]


def create_tenant(db: Session, payload: CreateTenantRequest):

  existing = db.query(TenantModel).filter(TenantModel.domain == payload.domain).first()
  if existing:
      return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"success": False,"message": "Tenant creation failed","details": f"Domain '{payload.domain}' already exists."}
      )
  new_tenant = TenantModel(**payload.model_dump())
  db.add(new_tenant)
  db.commit()
  db.refresh(new_tenant)
  return TenantResponse.model_validate(new_tenant)  