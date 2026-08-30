from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.config import settings

_checkpointer_cm = None
_checkpointer = None

async def get_checkpointer():
    """Postgres-backed persistent memory — async, ainvoke/astream ke saath compatible."""
    global _checkpointer_cm, _checkpointer
    
    if _checkpointer is None:
        _checkpointer_cm = AsyncPostgresSaver.from_conn_string(settings.postgres_url)
        _checkpointer = await _checkpointer_cm.__aenter__()
        await _checkpointer.setup()
    
    return _checkpointer