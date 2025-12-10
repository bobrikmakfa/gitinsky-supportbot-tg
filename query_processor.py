"""Query processor for analyzing and responding to user queries."""

import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from models import InteractionLog
from database import get_db
from knowledge_base import get_kb_manager
from deepseek_client import get_deepseek_client

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Process user queries and generate responses."""
    
    def __init__(self):
        """Initialize query processor."""
        self.kb_manager = get_kb_manager()
        self.deepseek_client = get_deepseek_client()
    
    async def process_query(
        self,
        telegram_id: int,
        query: str
    ) -> Dict[str, Any]:
        """
        Process user query and generate response.
        
        Args:
            telegram_id: Telegram user ID
            query: User's question
            
        Returns:
            Dictionary with response data
        """
        # Identify technologies in query
        identified_techs = self.kb_manager.identify_technologies(query)
        logger.info(f"Identified technologies: {identified_techs}")
        
        # Retrieve relevant knowledge
        knowledge_context = self.kb_manager.search_knowledge(query)
        
        # Generate AI response
        ai_result = await self.deepseek_client.generate_response(
            user_query=query,
            knowledge_context=knowledge_context
        )
        
        if not ai_result['success']:
            # Use fallback response
            response_text = self.deepseek_client.get_fallback_response()
            tokens_used = 0
            response_time_ms = ai_result.get('response_time_ms', 0)
        else:
            response_text = ai_result['response']
            tokens_used = ai_result['tokens_used']
            response_time_ms = ai_result['response_time_ms']
        
        # Log interaction
        try:
            with get_db() as db:
                log_entry = InteractionLog(
                    log_id=str(uuid.uuid4()),
                    telegram_id=telegram_id,
                    query=query,
                    response=response_text,
                    technologies_identified=identified_techs,
                    deepseek_tokens_used=tokens_used,
                    response_time_ms=response_time_ms
                )
                db.add(log_entry)
                db.commit()
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
        
        return {
            'success': True,
            'response': response_text,
            'technologies': identified_techs,
            'tokens_used': tokens_used
        }
    
    def format_response_for_telegram(self, response: str) -> str:
        """
        Format response text for Telegram markdown.
        
        Args:
            response: Raw response text
            
        Returns:
            Formatted response for Telegram
        """
        # Telegram supports markdown, but we need to be careful with special characters
        # For now, return as-is. Can be enhanced later with better formatting
        return response


# Global query processor instance
_query_processor: Optional[QueryProcessor] = None


def get_query_processor() -> QueryProcessor:
    """Get or create query processor instance."""
    global _query_processor
    if _query_processor is None:
        _query_processor = QueryProcessor()
    return _query_processor
