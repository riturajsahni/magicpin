import logging
from fastapi import APIRouter, HTTPException
from models.schemas import ReplyRequest, ReplyResponse
from services import memory, engagement_engine, intent_detector, ai_engine

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/reply", response_model=ReplyResponse)
async def reply(req: ReplyRequest) -> ReplyResponse:
    """Receive a merchant message and return Vera's intelligent reply."""
    ctx = memory.get_context(req.merchant_id)
    if not ctx:
        raise HTTPException(status_code=404, detail=f"No context found for merchant_id={req.merchant_id}")

    # Detect intent
    intent = intent_detector.detect_intent(req.message)
    logger.info("reply: merchant_id=%s intent=%s", req.merchant_id, intent)

    # Save merchant message to history
    memory.add_message(req.merchant_id, "user", req.message)

    history = memory.get_history(req.merchant_id)
    prompt  = engagement_engine.build_reply_prompt(ctx, history, req.message, intent)

    try:
        vera_reply = "TEST REPLY FROM VERA"
    except Exception as exc:
    logger.exception("AI generation failed during reply: %s", exc)
    raise HTTPException(
        status_code=502,
        detail=f"AI generation failed: {str(exc)}"
    )

    # Save Vera's reply to history
    memory.add_message(req.merchant_id, "assistant", vera_reply)

    return ReplyResponse(reply=vera_reply, intent=intent, merchant_id=req.merchant_id)
