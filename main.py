"""
Magicpin Merchant AI — FastAPI entry point.
Run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import context, tick, reply, health, metadata

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Magicpin Merchant AI (Vera)",
    description="AI-powered proactive merchant engagement assistant.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
PREFIX = "/v1"

app.include_router(context.router,  prefix=PREFIX, tags=["Context"])
app.include_router(tick.router,     prefix=PREFIX, tags=["Tick"])
app.include_router(reply.router,    prefix=PREFIX, tags=["Reply"])
app.include_router(health.router,   prefix=PREFIX, tags=["Health"])
app.include_router(metadata.router, prefix=PREFIX, tags=["Metadata"])


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Vera is online — Magicpin Merchant AI v1.0.0")
