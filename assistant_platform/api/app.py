from __future__ import annotations

from fastapi import FastAPI

# Ensure tool modules register themselves.
import assistant_platform.tools  # noqa: F401
from assistant_platform.api.routes_chat import router as chat_router
from assistant_platform.api.routes_gemma_table import router as gemma_table_router
from assistant_platform.api.routes_webhook import router as webhook_router

app = FastAPI(title="Assistant Platform V1")
app.include_router(chat_router)
app.include_router(gemma_table_router)
app.include_router(webhook_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"name": "assistant-platform", "status": "ready"}
