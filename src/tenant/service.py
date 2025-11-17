from typing import List
from sqlalchemy.orm import Session
from src.db.entities.TenantModel import TenantModel
from .models import TenantResponse, CreateTenantRequest

def get_all_tenants(db: Session) -> List[TenantResponse]:
  tenants = db.query(TenantModel).all()
  return [TenantResponse.model_validate(t) for t in tenants]


def create_tenant(db: Session, payload: CreateTenantRequest):
  new_tenant = TenantModel(**payload.model_dump())
  db.add(new_tenant)
  db.commit()
  db.refresh(new_tenant)
  return TenantResponse.model_validate(new_tenant)  