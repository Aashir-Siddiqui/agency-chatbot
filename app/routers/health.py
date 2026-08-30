from fastapi import APIRouter
from app.models.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Load balancers/monitoring tools isse ping karte hain"""
    return HealthResponse(status="healthy")