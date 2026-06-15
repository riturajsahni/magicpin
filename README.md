# Magicpin Merchant AI — Vera 🤖

A production-ready FastAPI application that powers **Vera**, an AI business growth consultant that proactively engages merchants on WhatsApp.

---

## Project Structure

```
magicpin_ai/
├── main.py                      # FastAPI app + router registration
├── routes/
│   ├── context.py               # POST /v1/context
│   ├── tick.py                  # POST /v1/tick
│   ├── reply.py                 # POST /v1/reply
│   ├── health.py                # GET  /v1/healthz
│   └── metadata.py              # GET  /v1/metadata
├── services/
│   ├── memory.py                # In-memory dictionary storage
│   ├── ai_engine.py             # OpenAI async wrapper
│   ├── engagement_engine.py     # Prompt building + category levers
│   ├── intent_detector.py       # Rule-based intent detection
│   └── context_manager.py      # Context persistence logic
├── models/
│   └── schemas.py               # Pydantic request/response models
├── prompts/
│   └── vera_system_prompt.txt   # Vera's system prompt reference
├── judge_simulator.py           # Local test script mimicking judge flow
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set your OpenAI API key

```bash
export OPENAI_API_KEY=sk-...    # Linux/Mac
set OPENAI_API_KEY=sk-...       # Windows CMD
```

Optionally set the model (defaults to `gpt-4o-mini`):

```bash
export OPENAI_MODEL=gpt-4o-mini
```

### 3. Run the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server runs at: **http://localhost:8000**
Interactive docs: **http://localhost:8000/docs**

### 4. Run the judge simulator

In a separate terminal (server must be running):

```bash
python judge_simulator.py
```

---

## API Reference

### `GET /v1/healthz`

```json
{ "status": "ok" }
```

### `GET /v1/metadata`

```json
{ "name": "Magicpin Merchant AI", "version": "1.0" }
```

---

### `POST /v1/context`

Store all merchant, category, trigger, and customer context.

**Request:**
```json
{
  "merchant": {
    "merchant_id": "merchant_001",
    "name": "Dr. Meera",
    "business_name": "Meera Dental Clinic",
    "category": "dentist",
    "city": "Bangalore",
    "review_count": 35,
    "rating": 4.1,
    "profile_complete": false,
    "active_offers": 0,
    "monthly_orders": 80
  },
  "category": {
    "category": "dentist",
    "avg_reviews_in_category": 120,
    "top_performing_metrics": ["reviews", "photos"],
    "common_offers": ["free consultation", "whitening package"]
  },
  "trigger": {
    "trigger_type": "low_reviews",
    "trigger_value": "35",
    "urgency": "high"
  },
  "customer": {
    "segment": "returning",
    "preferences": ["morning slots"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "merchant_id": "merchant_001",
  "message": "Context stored successfully for Meera Dental Clinic."
}
```

---

### `POST /v1/tick`

Ask Vera if she wants to send a proactive message.

**Request:**
```json
{ "merchant_id": "merchant_001" }
```

**Response:**
```json
{
  "should_send": true,
  "trigger_type": "low_reviews",
  "message": "Hi Dr. Meera! Dental clinics with 100+ reviews typically attract 30% more new patients. You currently have 35 reviews — would you like a personalised 7-day review growth plan for your clinic?"
}
```

---

### `POST /v1/reply`

Send a merchant reply and receive Vera's intelligent response.

**Request:**
```json
{
  "merchant_id": "merchant_001",
  "message": "Yes, tell me more about the review plan"
}
```

**Response:**
```json
{
  "merchant_id": "merchant_001",
  "intent": "interested",
  "reply": "Great, Dr. Meera! Here's a simple 7-day plan: Days 1-2, ask your satisfied patients to leave a Google review via WhatsApp. Days 3-5, respond to every existing review on Magicpin. Days 6-7, add 5 new before/after photos to your profile. This combination typically adds 15-25 reviews in a week. Shall I create a message template you can send to patients?"
}
```

---

## Supported Trigger Types

| Trigger Type         | Description                              |
|----------------------|------------------------------------------|
| `low_reviews`        | Merchant has fewer reviews than category avg |
| `festival`           | Upcoming festival opportunity            |
| `profile_incomplete` | Key profile fields missing               |
| `low_rating`         | Rating below category benchmark          |
| `no_active_offers`   | No current promotional offers            |
| `general`            | Default engagement                       |

## Supported Categories & Growth Levers

| Category   | Key Levers                                           |
|------------|------------------------------------------------------|
| Dentist    | reviews, whitening promotions, patient retention     |
| Restaurant | festival offers, combo meals, repeat customers       |
| Gym        | membership drives, referral campaigns                |
| Salon      | beauty packages, seasonal promotions, loyalty        |
| Pharmacy   | repeat medicine reminders, health awareness          |

## Detected Intents

| Intent           | Example Phrases                          |
|------------------|------------------------------------------|
| `interested`     | "yes", "sure", "please", "okay"          |
| `no`             | "no", "not interested", "no thanks"     |
| `pricing`        | "how much", "cost", "fee", "free?"      |
| `confused`       | "don't understand", "explain", "what"  |
| `greeting`       | "hello", "hi", "hey", "namaste"         |
| `request_details`| "tell me more", "details", "how"        |
| `campaign_help`  | "campaign", "offer", "promotion"        |
| `review_help`    | "review", "rating", "star"              |
| `profile_help`   | "profile", "update", "photo"            |
| `general`        | (fallback for unmatched messages)        |

---

## Environment Variables

| Variable         | Default         | Description                  |
|------------------|-----------------|------------------------------|
| `OPENAI_API_KEY` | *(required)*    | Your OpenAI secret key       |
| `OPENAI_MODEL`   | `gpt-4o-mini`   | Model to use for generation  |
