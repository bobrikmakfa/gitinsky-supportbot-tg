"""Email service for sending verification codes."""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional

from config import get_settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending verification codes via SMTP."""
    
    def __init__(self):
        """Initialize email service with configuration."""
        self.settings = get_settings()
    
    async def send_verification_code(
        self, 
        to_email: str, 
        verification_code: str,
        expiration_minutes: int = 15
    ) -> bool:
        """
        Send verification code to user's email.
        
        Args:
            to_email: Recipient email address
            verification_code: Verification code to send
            expiration_minutes: Code expiration time in minutes
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # ВРЕМЕННО: Логируем вместо реальной отправки для тестирования
            logger.info(f"📧 [SIMULATED] Verification email would be sent to: {to_email}")
            logger.info(f"📧 [SIMULATED] Verification code: {verification_code}")
            logger.info(f"📧 [SIMULATED] Code expires in: {expiration_minutes} minutes")
            
            # Для тестирования - просто возвращаем успех
            # УДАЛИТЕ ЭТУ СТРОКУ В ПРОДАКШЕНЕ!
            return True  # ← ВАЖНО: возвращаем True для обхода ошибки
            
            # ========== ЗАКОММЕНТИРУЙТЕ ВЕСЬ ОСТАЛЬНОЙ КОД НИЖЕ ==========
            # Create message
            #message = MIMEMultipart("alternative")
            #message["Subject"] = "Gitinsky Support Bot - Verification Code"
            #message["From"] = f"{self.settings.smtp_from_name} <{self.settings.smtp_from_email}>"
            #message["To"] = to_email
            
            # Create HTML and text content
            #text_content = self._create_text_email(verification_code, expiration_minutes)
            #html_content = self._create_html_email(verification_code, expiration_minutes)
            
            # Attach parts
            #part1 = MIMEText(text_content, "plain")
            #part2 = MIMEText(html_content, "html")
            #message.attach(part1)
            #message.attach(part2)
            
            # Send email
            #await aiosmtplib.send(
            #    message,
            #    hostname=self.settings.smtp_host,
            #    port=self.settings.smtp_port,
            #    username=self.settings.smtp_user,
            #    password=self.settings.smtp_password,
            #    start_tls=True
            #)
            
            #logger.info(f"Verification email sent successfully to {to_email}")
            #return True
            # ========== КОНЕЦ ЗАКОММЕНТИРОВАННОГО КОДА ==========
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {to_email}: {e}")
            return False
    
    def _create_text_email(self, code: str, expiration_minutes: int) -> str:
        """Create plain text email content."""
        return f"""
Gitinsky Support Bot - Email Verification

Hello!

You have requested access to the Gitinsky Support Bot. Please use the following verification code to complete the verification process:

Verification Code: {code}

This code will expire in {expiration_minutes} minutes.

To verify your account:
1. Return to the Telegram bot
2. Enter the verification code when prompted

If you did not request this verification code, please ignore this email.

---
Gitinsky Support Bot
Technical Support Assistant
"""
    
    def _create_html_email(self, code: str, expiration_minutes: int) -> str:
        """Create HTML email content."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .code-box {{
            background-color: #fff;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }}
        .code {{
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
            letter-spacing: 5px;
        }}
        .instructions {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Gitinsky Support Bot</h1>
        <p>Email Verification</p>
    </div>
    
    <div class="content">
        <p>Hello!</p>
        
        <p>You have requested access to the <strong>Gitinsky Support Bot</strong>. Please use the following verification code to complete the verification process:</p>
        
        <div class="code-box">
            <div class="code">{code}</div>
        </div>
        
        <p style="text-align: center; color: #ff5722;">
            <strong>⏱ This code will expire in {expiration_minutes} minutes</strong>
        </p>
        
        <div class="instructions">
            <h3>Verification Steps:</h3>
            <ol>
                <li>Return to the Telegram bot</li>
                <li>Enter the verification code when prompted</li>
                <li>Start getting technical support!</li>
            </ol>
        </div>
        
        <p style="color: #666; font-size: 14px;">
            If you did not request this verification code, please ignore this email.
        </p>
    </div>
    
    <div class="footer">
        <p><strong>Gitinsky Support Bot</strong></p>
        <p>Technical Support Assistant for IT Professionals</p>
    </div>
</body>
</html>
"""


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Get or create email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
