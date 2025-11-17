from typing import List
from sqlalchemy.orm import Session
from src.db.entities.TenantModel import TenantModel
from . import models

def get_all_tenants(db: Session) -> List[models.TenantResponse]:
  tenants = db.query(TenantModel).all()
  return [models.TenantResponse.model_validate(t) for t in tenants]
