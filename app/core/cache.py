from langchain_core.globals import set_llm_cache
from langchain_community.cache import RedisCache
from redis import Redis
from app.config import settings

def setup_cache():
    """Redis cache setup — FAQ-type queries ke liye cost/latency bachata hai"""
    if settings.redis_url:
        redis_client = Redis.from_url(settings.redis_url)
    else:
        redis_client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=0
        )
    cache = RedisCache(redis_=redis_client, ttl=3600)
    set_llm_cache(cache)