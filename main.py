import os
from datetime import datetime
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Caching Imports
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    print("🚀 Cache initialized successfully!")
    yield

app = FastAPI(title="n8n Workflow Popularity API", lifespan=lifespan)
engine = create_engine(os.getenv("DATABASE_URL"))

# --- FIXED: This route stops the "Not Found" error at http://127.0.0.1:8000/ ---
@app.get("/")
def home():
    return {
        "message": "Welcome to the n8n Popularity API!",
        "status": "Online",
        "how_to_use": "Visit /docs for the interactive dashboard or /api/v1/workflows for data."
    }

# --- FIXED: Standardized Query parameters to avoid 422 errors ---
@app.get("/api/v1/workflows")
@cache(expire=3600)
def get_ranked_workflows(
    platform: str = Query(None, description="e.g., YouTube"), 
    country: str = Query("Global", description="e.g., US or IN"), 
    limit: int = Query(10, ge=1, le=100)
):
    query_str = "SELECT workflow_name, platform, composite_score, country_code, popularity_metrics FROM workflows"
    filters = []
    params = {"limit": limit, "country": country}

    if platform:
        filters.append("platform = :platform")
        params["platform"] = platform
    if country:
        filters.append("country_code = :country")

    if filters:
        query_str += " WHERE " + " AND ".join(filters)

    query_str += " ORDER BY composite_score DESC LIMIT :limit"

    with engine.connect() as conn:
        result = conn.execute(text(query_str), params)
        workflows = [dict(row._mapping) for row in result]

    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "count": len(workflows),
        "data": workflows
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)