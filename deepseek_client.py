"""DeepSeek API client for AI-powered responses."""

import time
import logging
from typing import Optional, Dict, Any, List
import httpx
from openai import OpenAI

from config import get_settings

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """Client for DeepSeek API integration."""
    
    def __init__(self):
        """Initialize DeepSeek client."""
        self.settings = get_settings()
        
        # Проверяем наличие API ключа
        if not self.settings.openrouter_api_key:
            logger.error("OPENROUTER_API_KEY not found in configuration!")
            # Не падаем, чтобы бот мог работать без AI
            self.client = None
        else:
            # Инициализируем OpenAI client для DeepSeek API
            self.client = OpenAI(
                api_key=self.settings.openrouter_api_key,
                base_url=self.settings.deepseek_api_url or "https://api.deepseek.com",
                timeout=httpx.Timeout(self.settings.api_timeout_seconds or 30.0)
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
        base_prompt = """Ты технический ассистент поддержки для компании Gitinsky. 
Твоя роль - помогать сотрудникам компании с техническими вопросами, связанными со стеками технологий, используемыми в проектах.

Твои обязанности:
- Предоставлять точную, краткую техническую помощь
- Фокусироваться на практических решениях и лучших практиках
- Использовать четкий, профессиональный язык (русский)
- Если не уверен, признай это и предложи альтернативные ресурсы
- Форматировать сниппеты кода четко с правильным синтаксисом
- Предоставлять пошаговые инструкции, когда это уместно

Области технологий, которые ты поддерживаешь:
- Оркестрация: Ansible, Kubernetes, OpenShift, Puppet
- Контейнеризация: Docker, Docker Swarm, Docker Compose
- Infrastructure as Code: Terraform
- CI/CD: Argo CD, GitLab CI
- Мониторинг и логирование: ELK Stack, Zabbix, Grafana, Prometheus
- Базы данных: MySQL, PostgreSQL
- Сети: Cisco, Mikrotik, Keenetic
- Операционные системы: Linux, Windows Administration
- Программирование: Python
- Системное администрирование
"""
        
        if knowledge_context:
            base_prompt += f"\n\nРелевантная информация из базы знаний компании:\n{knowledge_context}"
        
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
            Dictionary with response data
        """
        # Если нет клиента (нет API ключа), сразу возвращаем ошибку
        if self.client is None:
            return {
                'success': False,
                'response': '',
                'tokens_used': 0,
                'response_time_ms': 0,
                'error': 'No API key configured'
            }
        
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
                    max_tokens=getattr(self.settings, 'max_response_tokens', 1000),
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
                
            except Exception as e:
                logger.error(f"API error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                
                return {
                    'success': False,
                    'response': '',
                    'tokens_used': 0,
                    'response_time_ms': int((time.time() - start_time) * 1000),
                    'error': str(e)
                }
    
    async def get_simple_response(self, query: str) -> str:
        """
        Simple method to get AI response (for use in bot).
        
        Args:
            query: User's question
            
        Returns:
            AI response or fallback message
        """
        result = await self.generate_response(query)
        
        if result['success']:
            return result['response']
        else:
            # Fallback message in Russian
            return """Испытываю технические трудности при подключении к AI-сервису в данный момент.

Пожалуйста:
1. Попробуйте задать вопрос еще раз через несколько минут
2. Переформулируйте вопрос
3. Обратитесь напрямую к вашему team lead или системному администратору
4. Проверьте нашу внутреннюю документацию или wiki

Приношу извинения за неудобства!"""


# Global DeepSeek client instance
_deepseek_client: Optional[DeepSeekClient] = None


def get_deepseek_client() -> DeepSeekClient:
    """Get or create DeepSeek client instance."""
    global _deepseek_client
    if _deepseek_client is None:
        _deepseek_client = DeepSeekClient()
    return _deepseek_client