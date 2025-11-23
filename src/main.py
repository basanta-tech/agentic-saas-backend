from fastapi import FastAPI
from src.api import register_routes
from src.logging import LogLevels, configure_logging
from src.db.core import settings
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
  configure_logging(LogLevels.info)

  app = FastAPI(
    title="Agentic SAAS for Multilingual Agents",
    version="1.0.0"
  )

  app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(settings.FRONTEND_URL)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )
  register_routes(app)
  return app


app = create_app()
