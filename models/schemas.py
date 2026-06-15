from pydantic import BaseModel, Field
from typing import Optional, Any


# ── Context endpoint ──────────────────────────────────────────────────────────

class MerchantContext(BaseModel):
    merchant_id: str
    name: str
    business_name: str
    category: str
    phone: Optional[str] = None
    city: Optional[str] = None
    review_count: Optional[int] = None
    rating: Optional[float] = None
    profile_complete: Optional[bool] = True
    active_offers: Optional[int] = 0
    monthly_orders: Optional[int] = None
    extra: Optional[dict[str, Any]] = None


class CategoryContext(BaseModel):
    category: str
    sub_category: Optional[str] = None
    avg_reviews_in_category: Optional[int] = None
    top_performing_metrics: Optional[list[str]] = None
    common_offers: Optional[list[str]] = None


class TriggerContext(BaseModel):
    trigger_type: str                   # e.g. "low_reviews", "festival", "profile_incomplete"
    trigger_value: Optional[str] = None # e.g. "Diwali", "35"
    urgency: Optional[str] = "medium"   # low / medium / high
    details: Optional[dict[str, Any]] = None


class CustomerContext(BaseModel):
    customer_id: Optional[str] = None
    segment: Optional[str] = None       # e.g. "new", "returning", "vip"
    last_visit: Optional[str] = None
    preferences: Optional[list[str]] = None


class ContextRequest(BaseModel):
    merchant: MerchantContext
    category: CategoryContext
    trigger: TriggerContext
    customer: Optional[CustomerContext] = None


class ContextResponse(BaseModel):
    success: bool
    merchant_id: str
    message: str


# ── Tick endpoint ─────────────────────────────────────────────────────────────

class TickRequest(BaseModel):
    merchant_id: str


class TickResponse(BaseModel):
    should_send: bool
    message: Optional[str] = None
    trigger_type: Optional[str] = None


# ── Reply endpoint ────────────────────────────────────────────────────────────

class ReplyRequest(BaseModel):
    merchant_id: str
    message: str


class ReplyResponse(BaseModel):
    reply: str
    intent: str
    merchant_id: str


# ── Health / Metadata ─────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str = "ok"


class MetadataResponse(BaseModel):
    name: str = "Magicpin Merchant AI"
    version: str = "1.0"
