"""
Converts raw Pydantic models into a flat dict and persists via memory service.
"""

import logging
from models.schemas import ContextRequest
from services import memory

logger = logging.getLogger(__name__)


def save_context(req: ContextRequest) -> str:
    merchant_id = req.merchant.merchant_id

    payload = {
        "merchant": req.merchant.model_dump(),
        "category": req.category.model_dump(),
        "trigger": req.trigger.model_dump(),
        "customer": req.customer.model_dump() if req.customer else {},
    }

    memory.store_context(merchant_id, payload)
    logger.info("Context stored for merchant_id=%s trigger=%s", merchant_id, req.trigger.trigger_type)
    return merchant_id


def get_full_context(merchant_id: str) -> dict | None:
    return memory.get_context(merchant_id)
