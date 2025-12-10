"""DeepSeek API client for AI-powered responses."""

import time
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI, APIError, APITimeoutError, RateLimitError
import httpx

from config import get_settings

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """Client for DeepSeek API integration."""
    
    def __init__(self):
        """Initialize DeepSeek client."""
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.deepseek_api_key,
            base_url=self.settings.deepseek_api_url,
            timeout=httpx.Timeout(self.settings.api_timeout_seconds)
        )
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def _create_system_prompt(self, knowledge_context: str = "") -> str:
        """
        Create system prompt for DeepSeek.
        
        Args:
            knowledge_context: Relevant knowledge base context
            
        Returns:
            System prompt string
        """
        base_prompt = """You are a technical support assistant for Gitinsky, an IT company. 
Your role is to help company employees with technical questions related to the technology stacks used in projects.

Your responsibilities:
- Provide accurate, concise technical assistance
- Focus on practical solutions and best practices
- Use clear, professional language
- If you're unsure, acknowledge it and suggest alternative resources
- Format code snippets clearly with proper syntax
- Provide step-by-step instructions when appropriate

Technology areas you support:
- Orchestration: Ansible, Kubernetes, OpenShift, Puppet
- Containerization: Docker, Docker Swarm, Docker Compose
- Infrastructure as Code: Terraform
- CI/CD: Argo CD, GitLab CI
- Monitoring & Logging: ELK Stack, Zabbix, Grafana, Prometheus
- Databases: MySQL, PostgreSQL
- Networking: Cisco, Mikrotik, Keenetic
- Operating Systems: Linux, Windows Administration
- Programming: Python
- System Administration
"""
        
        if knowledge_context:
            base_prompt += f"\n\nRelevant company knowledge base:\n{knowledge_context}"
        
        return base_prompt
    
    async def generate_response(
        self,
        user_query: str,
        knowledge_context: str = "",
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response to user query.
        
        Args:
            user_query: User's technical question
            knowledge_context: Relevant knowledge from knowledge base
            conversation_history: Previous conversation messages
            
        Returns:
            Dictionary with response data:
            {
                'success': bool,
                'response': str,
                'tokens_used': int,
                'error': Optional[str]
            }
        """
        start_time = time.time()
        
        # Prepare messages
        messages = [
            {"role": "system", "content": self._create_system_prompt(knowledge_context)}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current query
        messages.append({"role": "user", "content": user_query})
        
        # Try with retries
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    max_tokens=self.settings.max_response_tokens,
                    temperature=0.7,
                    stream=False
                )
                
                response_time_ms = int((time.time() - start_time) * 1000)
                
                result = {
                    'success': True,
                    'response': response.choices[0].message.content,
                    'tokens_used': response.usage.total_tokens,
                    'response_time_ms': response_time_ms,
                    'error': None
                }
                
                logger.info(f"DeepSeek API call successful. Tokens: {result['tokens_used']}, Time: {response_time_ms}ms")
                return result
                
            except RateLimitError as e:
                logger.warning(f"Rate limit error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                return {
                    'success': False,
                    'response': '',
                    'tokens_used': 0,
                    'response_time_ms': int((time.time() - start_time) * 1000),
                    'error': 'Rate limit exceeded. Please try again in a moment.'
                }
                
            except APITimeoutError as e:
                logger.error(f"API timeout (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    continue
                return {
                    'success': False,
                    'response': '',
                    'tokens_used': 0,
                    'response_time_ms': int((time.time() - start_time) * 1000),
                    'error': 'Request timeout. Please try again.'
                }
                
            except APIError as e:
                logger.error(f"API error: {e}")
                return {
                    'success': False,
                    'response': '',
                    'tokens_used': 0,
                    'response_time_ms': int((time.time() - start_time) * 1000),
                    'error': f'API error: {str(e)}'
                }
                
            except Exception as e:
                logger.error(f"Unexpected error in DeepSeek API call: {e}")
                return {
                    'success': False,
                    'response': '',
                    'tokens_used': 0,
                    'response_time_ms': int((time.time() - start_time) * 1000),
                    'error': 'An unexpected error occurred. Please try again.'
                }
        
        # Should not reach here, but just in case
        return {
            'success': False,
            'response': '',
            'tokens_used': 0,
            'response_time_ms': int((time.time() - start_time) * 1000),
            'error': 'Failed after multiple retries.'
        }
    
    def get_fallback_response(self) -> str:
        """
        Get fallback response when API is unavailable.
        
        Returns:
            Fallback response message
        """
        return """I'm experiencing technical difficulties connecting to the AI service right now. 

Please try one of the following:
1. Try your question again in a few moments
2. Rephrase your question
3. Contact your team lead or system administrator directly
4. Check our internal documentation wiki

I apologize for the inconvenience!"""


# Global DeepSeek client instance
_deepseek_client: Optional[DeepSeekClient] = None


def get_deepseek_client() -> DeepSeekClient:
    """Get or create DeepSeek client instance."""
    global _deepseek_client
    if _deepseek_client is None:
        _deepseek_client = DeepSeekClient()
    return _deepseek_client
