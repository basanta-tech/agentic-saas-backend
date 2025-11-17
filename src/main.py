from fastapi import FastAPI
from src.api import register_routes
from src.logging import LogLevels, configure_logging


def create_app() -> FastAPI:
  configure_logging(LogLevels.info)

  app = FastAPI(
    title="Agentic SAAS for Multilingual Agents",
    version="1.0.0"
  )

  register_routes(app)
  return app


app = create_app()
