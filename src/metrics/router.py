from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

__all__ = ("router",)


router = APIRouter(
    prefix="/metrics",
    tags=["Prometheus"],
)


@router.get("")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
