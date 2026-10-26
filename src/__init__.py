from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.data.registry import build_datasources
from src.modules.health_module import HealthModule
from src.routes import api_router
from src.services.chat import ChatService
from src.utils import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    datasources = build_datasources()
    health = HealthModule()
    for name, source in datasources.items():
        try:
            source.connect()
        except Exception:
            # keep the API up; /health reports the datasource as degraded
            logger.exception("could not connect datasource %s", name)
        health.register(name, source.ping)
    app.state.datasources = datasources
    app.state.health = health
    app.state.chat = ChatService(list(datasources.values()))
    try:
        yield
    finally:
        for source in datasources.values():
            source.close()


def create_app() -> FastAPI:
    app = FastAPI(title="ai-app-project-template", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
