"""
In-memory storage for all merchant data and conversation history.
All data lives in module-level dictionaries — no external DB required.
"""

from typing import Any

# merchant_id → full context dict
_merchant_contexts: dict[str, dict[str, Any]] = {}

# merchant_id → list of {"role": "...", "content": "..."} dicts
_conversation_histories: dict[str, list[dict[str, str]]] = {}


# ── Writers ───────────────────────────────────────────────────────────────────

def store_context(merchant_id: str, context: dict[str, Any]) -> None:
    _merchant_contexts[merchant_id] = context


def add_message(merchant_id: str, role: str, content: str) -> None:
    if merchant_id not in _conversation_histories:
        _conversation_histories[merchant_id] = []
    _conversation_histories[merchant_id].append({"role": role, "content": content})


# ── Readers ───────────────────────────────────────────────────────────────────

def get_context(merchant_id: str) -> dict[str, Any] | None:
    return _merchant_contexts.get(merchant_id)


def get_history(merchant_id: str) -> list[dict[str, str]]:
    return _conversation_histories.get(merchant_id, [])


def context_exists(merchant_id: str) -> bool:
    return merchant_id in _merchant_contexts


def all_merchant_ids() -> list[str]:
    return list(_merchant_contexts.keys())
