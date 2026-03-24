from __future__ import annotations

from fastapi import FastAPI

from gemma_table.web import router as gemma_table_router

app = FastAPI(title="Gemma Table Fine-Tuning Lab")
app.include_router(gemma_table_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"name": "gemma-table-finetune-lab", "status": "ready"}
