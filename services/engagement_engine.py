"""
Engagement Engine — decides *whether* to send a proactive message and
builds a rich, context-specific prompt for the AI to generate it.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── Category-specific growth levers ──────────────────────────────────────────

CATEGORY_LEVERS: dict[str, list[str]] = {
    "dentist":    ["reviews", "whitening promotions", "patient retention", "appointment reminders"],
    "restaurant": ["festival offers", "combo meals", "repeat customers", "delivery visibility"],
    "gym":        ["membership drives", "referral campaigns", "seasonal discounts", "class schedules"],
    "salon":      ["beauty packages", "seasonal promotions", "loyalty programs", "photo gallery"],
    "pharmacy":   ["repeat medicine reminders", "health awareness campaigns", "home delivery", "OPD tie-ups"],
}


def _normalise_category(category: str) -> str:
    return category.lower().strip()


def get_levers(category: str) -> list[str]:
    return CATEGORY_LEVERS.get(_normalise_category(category), ["reviews", "offers", "engagement"])


# ── Proactive engagement decision ─────────────────────────────────────────────

def should_engage(ctx: dict[str, Any]) -> bool:
    """Simple heuristic: always engage if we have a valid trigger."""
    trigger = ctx.get("trigger", {})
    return bool(trigger.get("trigger_type"))


def build_proactive_prompt(ctx: dict[str, Any]) -> str:
    merchant  = ctx.get("merchant", {})
    category  = ctx.get("category", {})
    trigger   = ctx.get("trigger", {})

    name          = merchant.get("name", "there")
    biz           = merchant.get("business_name", "your business")
    cat           = merchant.get("category", category.get("category", "business"))
    reviews       = merchant.get("review_count", "N/A")
    rating        = merchant.get("rating", "N/A")
    avg_reviews   = category.get("avg_reviews_in_category", "N/A")
    trigger_type  = trigger.get("trigger_type", "general")
    trigger_value = trigger.get("trigger_value", "")
    urgency       = trigger.get("urgency", "medium")
    levers        = ", ".join(get_levers(cat))

    prompt = f"""
You are Vera, an AI business growth consultant for Magicpin merchants.

MERCHANT DETAILS:
- Name: {name}
- Business: {biz}
- Category: {cat}
- Reviews: {reviews} (category average: {avg_reviews})
- Rating: {rating}
- Trigger: {trigger_type} (value: {trigger_value}, urgency: {urgency})

CATEGORY GROWTH LEVERS FOR {cat.upper()}: {levers}

TASK:
Generate ONE proactive WhatsApp message from Vera to {name}.
- Address {name} by first name.
- Reference the specific trigger: {trigger_type} ({trigger_value}).
- Include one concrete, actionable insight or question.
- Keep it under 3 sentences.
- Tone: warm, professional, consultative.
- Never start with "Hello" alone. Lead with value.

Respond with ONLY the WhatsApp message. No labels, no explanation.
""".strip()

    return prompt


def build_reply_prompt(ctx: dict[str, Any], history: list[dict], merchant_message: str, intent: str) -> str:
    merchant = ctx.get("merchant", {})
    category = ctx.get("category", {})
    trigger  = ctx.get("trigger", {})

    name         = merchant.get("name", "there")
    biz          = merchant.get("business_name", "your business")
    cat          = merchant.get("category", category.get("category", "business"))
    reviews      = merchant.get("review_count", "N/A")
    rating       = merchant.get("rating", "N/A")
    trigger_type = trigger.get("trigger_type", "general")
    levers       = ", ".join(get_levers(cat))

    # Format conversation history (last 6 turns max to stay concise)
    history_text = ""
    for turn in history[-6:]:
        role = "Vera" if turn["role"] == "assistant" else name
        history_text += f"{role}: {turn['content']}\n"

    prompt = f"""
You are Vera, an AI business growth consultant for Magicpin merchants.

MERCHANT DETAILS:
- Name: {name}
- Business: {biz}
- Category: {cat}
- Reviews: {reviews}
- Rating: {rating}
- Active Trigger: {trigger_type}
- Growth Levers: {levers}

CONVERSATION SO FAR:
{history_text.strip() if history_text else "(No prior conversation)"}

MERCHANT'S LATEST MESSAGE: "{merchant_message}"
DETECTED INTENT: {intent}

TASK:
Reply as Vera.
- Keep response under 4 sentences.
- Be specific to {name}'s context — no generic advice.
- If intent is "interested" or "yes" → provide a concrete next step or mini-plan.
- If intent is "no" → gracefully acknowledge and leave the door open.
- If intent is "pricing" → clarify that Magicpin features are mostly free / low-cost and pivot to value.
- If intent is "confused" → simplify and re-explain.
- If intent is "greeting" → greet back and immediately pivot to their key growth opportunity.
- For any other intent → continue the conversation helpfully.

Respond with ONLY the WhatsApp reply. No labels, no explanation.
""".strip()

    return prompt
