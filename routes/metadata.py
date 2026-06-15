from fastapi import APIRouter
from models.schemas import MetadataResponse

router = APIRouter()


@router.get("/metadata", response_model=MetadataResponse)
async def metadata() -> MetadataResponse:
    return MetadataResponse(name="Magicpin Merchant AI", version="1.0")
