from fastapi import APIRouter, Request

from src.services.health import HealthService

router = APIRouter(tags=["health"])


@router.get("/health")
def health(request: Request) -> dict:
    return HealthService(request.app.state.health).status()
