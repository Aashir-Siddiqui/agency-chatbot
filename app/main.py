from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import chat, health
from app.middleware.rate_limit import limiter
from app.core.cache import setup_cache
from app.core.memory import get_checkpointer
from app.core.rag_chain import build_rag_graph
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Pixelo Digital AI Assistant",
    description="Production RAG chatbot for agency services and policies",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pixelodigital.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    setup_cache()
    checkpointer = await get_checkpointer()
    app.state.rag_graph = build_rag_graph(checkpointer)
    logging.info("Pixelo Bot started successfully")

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(health.router, tags=["health"])