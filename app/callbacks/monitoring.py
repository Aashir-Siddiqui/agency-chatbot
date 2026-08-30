from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict
from datetime import datetime
import logging

logger = logging.getLogger("pixelo_bot")

class ProductionMonitoringHandler(BaseCallbackHandler):
    """Cost tracking, error alerting, aur structured logging combine kiya"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.total_tokens = 0
    
    def on_llm_end(self, response, **kwargs: Any) -> None:
        if response.llm_output and "token_usage" in response.llm_output:
            tokens = response.llm_output["token_usage"].get("total_tokens", 0)
            self.total_tokens += tokens
            logger.info(f"[{self.session_id}] Tokens used: {tokens}")
    
    def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        logger.error(f"[{self.session_id}] LLM Error: {str(error)}")
    
    def on_retriever_end(self, documents, **kwargs: Any) -> None:
        logger.info(f"[{self.session_id}] Retrieved {len(documents)} documents")