from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: str = Field(..., description="Unique conversation/session identifier")

class ChatResponse(BaseModel):
    answer: str
    session_id: str

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"