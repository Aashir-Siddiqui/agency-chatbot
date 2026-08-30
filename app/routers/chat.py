from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.callbacks.monitoring import ProductionMonitoringHandler
from app.middleware.auth import verify_api_key
from app.middleware.rate_limit import limiter
import json

router = APIRouter()


@router.post("/chat/stream", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
async def stream_chat(request: Request, chat_request: ChatRequest):
    rag_graph = request.app.state.rag_graph
    config = {
        "configurable": {"thread_id": chat_request.session_id},
        "callbacks": [ProductionMonitoringHandler(session_id=chat_request.session_id)]
    }
    
    async def event_generator():
        try:
            async for event in rag_graph.astream_events(
                {"messages": [{"role": "user", "content": chat_request.message}]},
                version="v2",
                config=config
            ):
                if event["event"] == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield f"data: {json.dumps({'token': content})}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'error': 'Something went wrong. Please try again.'})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/chat", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
async def chat(request: Request, chat_request: ChatRequest):
    """Non-streaming version — mobile apps ke liye simpler ho sakta hai"""
    rag_graph = request.app.state.rag_graph
    config = {
        "configurable": {"thread_id": chat_request.session_id},
        "callbacks": [ProductionMonitoringHandler(session_id=chat_request.session_id)]
    }
    
    result = await rag_graph.ainvoke(
        {"messages": [{"role": "user", "content": chat_request.message}]},
        config=config
    )
    
    return {
        "answer": result["messages"][-1].content,
        "session_id": chat_request.session_id
    }