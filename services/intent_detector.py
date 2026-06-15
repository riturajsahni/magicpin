"""
Lightweight intent detection — rule-based keyword matching as primary layer,
with a clear extension point for LLM-based fallback.
"""

import re

# intent → list of keyword patterns (lowercased)
_RULES: dict[str, list[str]] = {
    "interested":      [r"\byes\b", r"\bsure\b", r"\binterested\b", r"\bplease\b", r"\bgo ahead\b", r"\bokay\b", r"\bok\b"],
    "no":              [r"\bno\b", r"\bnot interested\b", r"\bno thanks\b", r"\bnope\b", r"\bdont want\b", r"\bdon't want\b"],
    "pricing":         [r"\bhow much\b", r"\bprice\b", r"\bcost\b", r"\bfee\b", r"\bpaid\b", r"\bfree\b", r"\bcharge\b"],
    "confused":        [r"\bwhat\b", r"\bdon't understand\b", r"\bconfused\b", r"\bhow does\b", r"\bexplain\b"],
    "greeting":        [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgood morning\b", r"\bgood evening\b", r"\bnamaste\b"],
    "request_details": [r"\btell me more\b", r"\bmore details\b", r"\bmore info\b", r"\bdetails\b", r"\bhow\b"],
    "campaign_help":   [r"\bcampaign\b", r"\boffer\b", r"\bpromotion\b", r"\bdeal\b", r"\bdiscount\b"],
    "review_help":     [r"\breview\b", r"\brating\b", r"\bfeedback\b", r"\bstar\b"],
    "profile_help":    [r"\bprofile\b", r"\bupdate\b", r"\bphoto\b", r"\bimage\b", r"\bdescription\b"],
}


def detect_intent(message: str) -> str:
    """Return the best-matching intent string."""
    text = message.lower().strip()

    for intent, patterns in _RULES.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent

    return "general"
