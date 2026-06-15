from fastapi import APIRouter
from models.schemas import HealthResponse, MetadataResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
