from typing import List
from fastapi import APIRouter, status
from ..db.core import DbSession
from . import models
from . import service
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/tenants",
  tags=["Tenants"]
)

@router.get("/", response_model=List[models.TenantResponse])
def get_tenants(db: DbSession):
  return service.get_all_tenants(db)