from __future__ import annotations

import os
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Ensure backend package is importable when running from project root
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_ROOT = CURRENT_DIR.parent
PROJECT_ROOT = BACKEND_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import services
from backend.similarity_service.main import initialize_database as init_db  # type: ignore
from backend.similarity_service.game_queries import (  # type: ignore
    find_similar_games,
)


app = FastAPI(title="IPUM Lab GUI API", version="0.1.0")


class GamesSearchRequest(BaseModel):
    description: str = Field(..., min_length=1)
    min_score: Optional[float] = None
    max_price: Optional[float] = None
    windows: Optional[bool] = None
    linux: Optional[bool] = None
    mac: Optional[bool] = None
    limit: int = 5


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "backend": "fastapi",
        "db_host": os.getenv("DB_HOST", "localhost"),
    }


@app.post("/api/similarity/games/search")
def api_similarity_games_search(payload: GamesSearchRequest) -> list[dict[str, Any]]:
    try:
        results = find_similar_games(
            description=payload.description,
            min_score=payload.min_score,
            max_price=payload.max_price,
            windows=payload.windows,
            linux=payload.linux,
            mac=payload.mac,
            limit=payload.limit,
        )
    except Exception as exc:  # pragma: no cover - surface error to client
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return [
        {
            "id": game.id,
            "name": game.name,
            "price": game.price,
            "windows": game.windows,
            "linux": game.linux,
            "mac": game.mac,
            "description": game.description[:300] if game.description else "",
        }
        for game in results
    ]


@app.post("/api/similarity/setup")
def api_similarity_setup() -> dict[str, Any]:
    try:
        init_db()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"status": "ok", "message": "Database tables created"}


# Minimal RAG placeholder endpoints
class RagAskRequest(BaseModel):
    question: str


@app.post("/api/rag/ask")
def api_rag_ask(payload: RagAskRequest) -> dict[str, Any]:
    # TODO: Wire into lab_rag pipeline if available as callable module
    # For now, return a stub response so the GUI can be built
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="question is required")
    return {
        "answer": f"[stub] You asked: '{payload.question}'. Connect this to lab_rag to get real answers.",
        "sources": [],
    }


if __name__ == "__main__":  # Manual run convenience
    import uvicorn

    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
        reload=bool(int(os.getenv("API_RELOAD", "0"))),
    )


