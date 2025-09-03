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
# NOTE: Avoid importing heavy similarity modules at startup.
# We'll import them lazily inside endpoints to keep FastAPI light for health checks.


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
        from backend.similarity_service.game_queries import find_similar_games  # type: ignore
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
        from backend.similarity_service.main import initialize_database as init_db  # type: ignore
        init_db()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"status": "ok", "message": "Database tables created"}


# Minimal RAG placeholder endpoints
class RagAskRequest(BaseModel):
    question: str


class RagSetupRequest(BaseModel):
    pdf_url: str = Field(..., description="URL to PDF document")
    collection_name: str = Field(default="rag_texts_and_embeddings", description="Milvus collection name")


@app.post("/api/rag/ask")
def api_rag_ask(payload: RagAskRequest) -> dict[str, Any]:
    """Ask a question using RAG with Milvus vector search"""
    try:
        from backend.lab_rag.milvus_interface import MilvusInterface  # type: ignore
        
        # Initialize Milvus interface
        milvus = MilvusInterface()
        
        # Search for relevant context
        search_results = milvus.search(
            query=payload.question,
            collection_name="rag_texts_and_embeddings",
            limit=3  # Get top 3 most relevant pages
        )
        
        if not search_results or not search_results[0]:
            return {
                "answer": "Nie znalazłem odpowiednich informacji w bazie wiedzy.",
                "sources": [],
                "context": ""
            }
        
        # Extract context from search results
        context_parts = []
        for hit in search_results[0]:
            if "entity" in hit and "text" in hit["entity"]:
                context_parts.append(hit["entity"]["text"])
        
        context = "\n\n".join(context_parts)
        
        # For now, return context-based response (can be extended with LLM later)
        answer = f"Na podstawie znalezionych informacji:\n\n{context[:1000]}..."
        
        return {
            "answer": answer,
            "sources": [f"Page {i+1}" for i in range(len(context_parts))],
            "context": context,
            "question": payload.question
        }
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG error: {str(exc)}")


@app.post("/api/rag/setup")
def api_rag_setup(payload: RagSetupRequest) -> dict[str, Any]:
    """Setup RAG collection and process PDF document"""
    try:
        from backend.lab_rag.milvus_interface import MilvusInterface  # type: ignore
        
        milvus = MilvusInterface()
        
        # Generate filenames based on PDF URL
        pdf_name = payload.pdf_url.split("/")[-1]
        base_name = pdf_name.replace(".pdf", "")
        file_json = f"{base_name}.json"
        embeddings_json = f"{base_name}-Embeddings.json"
        
        # Create collection and process PDF
        milvus.create_rag_pipeline(
            pdf_url=payload.pdf_url,
            file_name=pdf_name,
            file_json=file_json,
            embeddings_json=embeddings_json,
            collection_name=payload.collection_name
        )
        
        return {
            "status": "success",
            "message": f"RAG pipeline completed for {pdf_name}",
            "collection": payload.collection_name,
            "files_created": [file_json, embeddings_json]
        }
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG setup error: {str(exc)}")


@app.get("/api/rag/collections")
def api_rag_collections() -> dict[str, Any]:
    """List available Milvus collections"""
    try:
        from backend.lab_rag.milvus_interface import MilvusInterface  # type: ignore
        
        milvus = MilvusInterface()
        collections = milvus.milvus_client.list_collections()
        
        return {
            "collections": collections,
            "count": len(collections)
        }
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error listing collections: {str(exc)}")


@app.delete("/api/rag/collections/{collection_name}")
def api_rag_delete_collection(collection_name: str) -> dict[str, Any]:
    """Delete a Milvus collection"""
    try:
        from backend.lab_rag.milvus_interface import MilvusInterface  # type: ignore
        
        milvus = MilvusInterface()
        milvus.remove_collection(collection_name)
        
        return {
            "status": "success",
            "message": f"Collection {collection_name} deleted"
        }
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error deleting collection: {str(exc)}")


if __name__ == "__main__":  # Manual run convenience
    import uvicorn

    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", "8000")),
        reload=bool(int(os.getenv("API_RELOAD", "0"))),
    )


