import logging
from fastapi import APIRouter, HTTPException
from models.schemas import TickRequest, TickResponse
from services import memory, engagement_engine, ai_engine

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/tick", response_model=TickResponse)
async def tick(req: TickRequest) -> TickResponse:
    """
    Judge asks: 'Do you want to send a proactive message?'
    We decide and generate one if appropriate.
    """
    ctx = memory.get_context(req.merchant_id)
    if not ctx:
        raise HTTPException(status_code=404, detail=f"No context found for merchant_id={req.merchant_id}")

    if not engagement_engine.should_engage(ctx):
        logger.info("tick: no engagement for merchant_id=%s", req.merchant_id)
        return TickResponse(should_send=False)

    trigger_type = ctx.get("trigger", {}).get("trigger_type", "general")
    prompt = engagement_engine.build_proactive_prompt(ctx)

    try:
        message = "TEST MESSAGE FROM VERA"
    except Exception as exc:
        logger.exception("AI generation failed during tick: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"AI generation failed: {str(exc)}"
    )

    # Store Vera's proactive message in history
    memory.add_message(req.merchant_id, "assistant", message)

    logger.info("tick: proactive message sent for merchant_id=%s trigger=%s", req.merchant_id, trigger_type)
    return TickResponse(should_send=True, message=message, trigger_type=trigger_type)
