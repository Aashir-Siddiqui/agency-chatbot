from fastapi import Header, HTTPException
from app.config import settings

async def verify_api_key(x_api_key: str = Header(...)):
    """Simple API key check — production mein JWT/OAuth bhi use kar sakte ho"""
    if x_api_key != settings.api_secret_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key