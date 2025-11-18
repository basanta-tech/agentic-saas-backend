from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic_settings import BaseSettings
from functools import cached_property


class Settings(BaseSettings):
  DB_USER: str | None = None
  DB_PASS: str | None = None
  DB_HOST: str | None = None
  DB_PORT: int | None = None
  DB_NAME: str | None = None
  LIVEKIT_API_KEY: str | None = None
  LIVEKIT_API_SECRET: str | None = None
  LIVEKIT_URL: str | None = None
  NEXT_PUBLIC_LIVEKIT_URL: str | None = None
  OPENAI_API_KEY: str | None = None
  GOOGLE_API_KEY: str | None = None
  
  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"

  @cached_property
  def DATABASE_URL(self) -> str:
    """Build the full database URL dynamically"""
    return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

engine = create_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
        
DbSession = Annotated[Session, Depends(get_db)]
