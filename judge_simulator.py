"""
judge_simulator.py — Simulates the Magicpin AI Challenge judge flow.

Usage:
  python judge_simulator.py

Requires the FastAPI server to be running on http://localhost:8000
"""

import json
import httpx

BASE = "http://localhost:8000/v1"


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def call(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{BASE}{path}"
    with httpx.Client(timeout=30) as client:
        if method == "GET":
            r = client.get(url)
        else:
            r = client.post(url, json=body)
    print(f"\n[{method}] {url}")
    if body:
        print("REQUEST:", json.dumps(body, indent=2))
    print(f"STATUS : {r.status_code}")
    data = r.json()
    print("RESPONSE:", json.dumps(data, indent=2))
    return data


# ── Health ─────────────────────────────────────────────────────────────────────
section("1. Health Check")
call("GET", "/healthz")

# ── Metadata ──────────────────────────────────────────────────────────────────
section("2. Metadata")
call("GET", "/metadata")

# ── Context ───────────────────────────────────────────────────────────────────
section("3. POST /context — Dentist with low reviews")
MERCHANT_ID = "merchant_001"
call("POST", "/context", {
    "merchant": {
        "merchant_id": MERCHANT_ID,
        "name": "Dr. Meera",
        "business_name": "Meera Dental Clinic",
        "category": "dentist",
        "phone": "+91-9876543210",
        "city": "Bangalore",
        "review_count": 35,
        "rating": 4.1,
        "profile_complete": False,
        "active_offers": 0,
        "monthly_orders": 80
    },
    "category": {
        "category": "dentist",
        "sub_category": "cosmetic dentistry",
        "avg_reviews_in_category": 120,
        "top_performing_metrics": ["reviews", "photos", "response_rate"],
        "common_offers": ["free consultation", "whitening package"]
    },
    "trigger": {
        "trigger_type": "low_reviews",
        "trigger_value": "35",
        "urgency": "high",
        "details": {"threshold": 100}
    },
    "customer": {
        "customer_id": "cust_001",
        "segment": "returning",
        "last_visit": "2024-12-01",
        "preferences": ["morning slots", "WhatsApp updates"]
    }
})

# ── Tick ───────────────────────────────────────────────────────────────────────
section("4. POST /tick — Proactive message")
call("POST", "/tick", {"merchant_id": MERCHANT_ID})

# ── Reply: interested ──────────────────────────────────────────────────────────
section("5. POST /reply — Merchant says 'Yes, tell me more'")
call("POST", "/reply", {"merchant_id": MERCHANT_ID, "message": "Yes, tell me more about the review plan"})

# ── Reply: pricing ────────────────────────────────────────────────────────────
section("6. POST /reply — Merchant asks about pricing")
call("POST", "/reply", {"merchant_id": MERCHANT_ID, "message": "How much does this cost?"})

# ── Reply: confused ────────────────────────────────────────────────────────────
section("7. POST /reply — Merchant is confused")
call("POST", "/reply", {"merchant_id": MERCHANT_ID, "message": "I don't understand what you mean"})

# ── New merchant: Restaurant + Festival trigger ────────────────────────────────
section("8. Restaurant merchant with festival trigger")
REST_ID = "merchant_002"
call("POST", "/context", {
    "merchant": {
        "merchant_id": REST_ID,
        "name": "Ravi",
        "business_name": "Ravi's Kitchen",
        "category": "restaurant",
        "city": "Delhi",
        "review_count": 210,
        "rating": 4.4,
        "profile_complete": True,
        "active_offers": 1,
        "monthly_orders": 350
    },
    "category": {
        "category": "restaurant",
        "avg_reviews_in_category": 180,
        "common_offers": ["combo meals", "festival specials"]
    },
    "trigger": {
        "trigger_type": "festival",
        "trigger_value": "Diwali",
        "urgency": "medium"
    }
})
call("POST", "/tick", {"merchant_id": REST_ID})
call("POST", "/reply", {"merchant_id": REST_ID, "message": "Interesting! What kind of offer should I run?"})

print("\n\n✅  Judge simulation complete.\n")
