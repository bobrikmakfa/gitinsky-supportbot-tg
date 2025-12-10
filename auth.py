"""Authentication module for user verification."""

import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging
from email_validator import validate_email, EmailNotValidError

from models import User, VerificationStatus
from database import get_db
from email_service import get_email_service
from config import get_settings

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Service for handling user authentication and verification."""
    
    def __init__(self):
        """Initialize authentication service."""
        self.settings = get_settings()
        self.email_service = get_email_service()
    
    def generate_verification_code(self, length: int = 6) -> str:
        """
        Generate a random verification code.
        
        Args:
            length: Length of the verification code
            
        Returns:
            Random verification code
        """
        characters = string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def validate_email_domain(self, email: str) -> Tuple[bool, str]:
        """
        Validate email address and check domain.
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate email format
            validated = validate_email(email, check_deliverability=False)
            email_normalized = validated.normalized
            
            # Check domain
            domain = email_normalized.split('@')[1]
            if domain.lower() != self.settings.company_email_domain.lower():
                return False, f"Email must be from {self.settings.company_email_domain} domain"
            
            return True, email_normalized
            
        except EmailNotValidError as e:
            return False, str(e)
    
    async def start_verification(self, telegram_id: int, username: Optional[str], email: str) -> Tuple[bool, str]:
        """
        Start email verification process for a user.
        
        Args:
            telegram_id: Telegram user ID
            username: Telegram username
            email: User's company email address
            
        Returns:
            Tuple of (success, message)
        """
        # Validate email domain
        is_valid, result = self.validate_email_domain(email)
        if not is_valid:
            return False, f"Invalid email: {result}"
        
        email_normalized = result
        
        with get_db() as db:
            # Check if user already exists with this email
            existing_user = db.query(User).filter(User.email == email_normalized).first()
            if existing_user and existing_user.telegram_id != telegram_id:
                return False, "This email is already registered to another user"
            
            # Get or create user
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if user is None:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    email=email_normalized,
                    verification_status=VerificationStatus.PENDING
                )
                db.add(user)
            else:
                user.email = email_normalized
                user.username = username
                user.verification_status = VerificationStatus.PENDING
            
            # Generate verification code
            verification_code = self.generate_verification_code()
            expiration = datetime.utcnow() + timedelta(minutes=self.settings.verification_code_ttl)
            
            user.verification_code = verification_code
            user.verification_code_expires_at = expiration
            
            db.commit()
            
            # Send verification email
            email_sent = await self.email_service.send_verification_code(
                email_normalized,
                verification_code,
                self.settings.verification_code_ttl
            )
            
            if not email_sent:
                return False, "Failed to send verification email. Please try again later."
            
            return True, f"Verification code sent to {email_normalized}"
    
    def verify_code(self, telegram_id: int, code: str) -> Tuple[bool, str]:
        """
        Verify the code provided by user.
        
        Args:
            telegram_id: Telegram user ID
            code: Verification code entered by user
            
        Returns:
            Tuple of (success, message)
        """
        with get_db() as db:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "User not found. Please start verification process with /verify"
            
            if user.verification_status == VerificationStatus.VERIFIED:
                return True, "You are already verified!"
            
            if not user.is_verification_code_valid():
                return False, "Verification code has expired. Please request a new code with /verify"
            
            if user.verification_code != code:
                return False, "Invalid verification code. Please try again."
            
            # Verify user
            user.verification_status = VerificationStatus.VERIFIED
            user.verified_at = datetime.utcnow()
            user.verification_code = None
            user.verification_code_expires_at = None
            
            db.commit()
            
            logger.info(f"User {telegram_id} successfully verified")
            return True, "✅ Verification successful! You can now use the bot."
    
    def check_user_verified(self, telegram_id: int) -> bool:
        """
        Check if user is verified.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            True if user is verified, False otherwise
        """
        with get_db() as db:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False
            
            # Check if session expired
            if user.is_session_expired(self.settings.session_ttl_days):
                user.verification_status = VerificationStatus.PENDING
                db.commit()
                return False
            
            return user.is_verified()
    
    def get_user_status(self, telegram_id: int) -> Tuple[bool, str]:
        """
        Get verification status for a user.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            Tuple of (exists, status_message)
        """
        with get_db() as db:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                return False, "❌ Not registered. Use /verify to start verification."
            
            if user.verification_status == VerificationStatus.VERIFIED:
                if user.is_session_expired(self.settings.session_ttl_days):
                    user.verification_status = VerificationStatus.PENDING
                    db.commit()
                    return True, "⚠️ Session expired. Please verify again with /verify"
                return True, f"✅ Verified\n📧 Email: {user.email}\n📅 Verified: {user.verified_at.strftime('%Y-%m-%d %H:%M UTC')}"
            
            elif user.verification_status == VerificationStatus.PENDING:
                if user.verification_code and user.is_verification_code_valid():
                    time_left = (user.verification_code_expires_at - datetime.utcnow()).seconds // 60
                    return True, f"⏳ Pending verification\n📧 Email: {user.email}\n⏱ Code expires in {time_left} minutes"
                return True, f"⏳ Pending verification\n📧 Email: {user.email}\nUse /verify to get a new code"
            
            else:  # REVOKED
                return True, "🚫 Access revoked. Contact administrator."
    
    def is_admin(self, telegram_id: int) -> bool:
        """
        Check if user is an administrator.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            True if user is admin, False otherwise
        """
        # Check if in admin list from config
        if telegram_id in self.settings.admin_telegram_ids:
            return True
        
        # Check database admin flag
        with get_db() as db:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            return user.is_admin if user else False
    
    def update_last_interaction(self, telegram_id: int):
        """
        Update user's last interaction timestamp.
        
        Args:
            telegram_id: Telegram user ID
        """
        with get_db() as db:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.last_interaction = datetime.utcnow()
                db.commit()


# Global authentication service instance
_auth_service: Optional[AuthenticationService] = None


def get_auth_service() -> AuthenticationService:
    """Get or create authentication service instance."""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthenticationService()
    return _auth_service
