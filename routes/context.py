import logging
from fastapi import APIRouter, HTTPException
from models.schemas import ContextRequest, ContextResponse
from services import context_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/context", response_model=ContextResponse)
async def receive_context(req: ContextRequest) -> ContextResponse:
    """Store merchant, category, trigger, and customer context."""
    try:
        merchant_id = context_manager.save_context(req)
        return ContextResponse(
            success=True,
            merchant_id=merchant_id,
            message=f"Context stored successfully for {req.merchant.business_name}.",
        )
    except Exception as exc:
        logger.exception("Failed to store context: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to store context.") from exc
