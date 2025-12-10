"""Database models for Gitinsky Support Bot."""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Enum as SQLEnum, JSON, ForeignKey, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum


Base = declarative_base()


class VerificationStatus(enum.Enum):
    """User verification status enumeration."""
    PENDING = "pending"
    VERIFIED = "verified"
    REVOKED = "revoked"


class FeedbackType(enum.Enum):
    """User feedback type enumeration."""
    HELPFUL = "helpful"
    NOT_HELPFUL = "not_helpful"


class TechnologyCategory(enum.Enum):
    """Technology category enumeration."""
    ORCHESTRATION = "orchestration"
    CONTAINERIZATION = "containerization"
    INFRASTRUCTURE_AS_CODE = "infrastructure_as_code"
    CI_CD = "ci_cd"
    MONITORING_LOGGING = "monitoring_logging"
    DATABASE = "database"
    NETWORKING = "networking"
    OPERATING_SYSTEM = "operating_system"
    PROGRAMMING = "programming"
    SYSTEM_ADMINISTRATION = "system_administration"


class User(Base):
    """User model for storing verified users."""
    
    __tablename__ = "users"
    
    # Primary key
    telegram_id = Column(Integer, primary_key=True, index=True)
    
    # User information
    username = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Verification
    verification_status = Column(
        SQLEnum(VerificationStatus),
        default=VerificationStatus.PENDING,
        nullable=False
    )
    verification_code = Column(String(10), nullable=True)
    verification_code_expires_at = Column(DateTime, nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    # Session management
    last_interaction = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Admin flag
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    interactions = relationship("InteractionLog", back_populates="user", cascade="all, delete-orphan")
    
    def is_verified(self) -> bool:
        """Check if user is verified."""
        return self.verification_status == VerificationStatus.VERIFIED
    
    def is_verification_code_valid(self) -> bool:
        """Check if verification code is still valid."""
        if not self.verification_code or not self.verification_code_expires_at:
            return False
        return datetime.utcnow() < self.verification_code_expires_at
    
    def is_session_expired(self, session_ttl_days: int = 30) -> bool:
        """Check if user session has expired."""
        if not self.last_interaction:
            return True
        expiry_date = self.last_interaction + timedelta(days=session_ttl_days)
        return datetime.utcnow() > expiry_date


class KnowledgeEntry(Base):
    """Knowledge base entry model."""
    
    __tablename__ = "knowledge_entries"
    
    # Primary key
    entry_id = Column(String(36), primary_key=True)
    
    # Technology information
    technology_name = Column(String(255), nullable=False, index=True)
    category = Column(SQLEnum(TechnologyCategory), nullable=False, index=True)
    
    # Content
    content = Column(Text, nullable=False)
    keywords = Column(JSON, nullable=False, default=list)  # List of keywords
    
    # Metadata
    version = Column(Integer, default=1, nullable=False)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for fast search
    __table_args__ = (
        Index('idx_technology_category', 'technology_name', 'category'),
    )


class InteractionLog(Base):
    """Interaction log model for tracking bot conversations."""
    
    __tablename__ = "interaction_logs"
    
    # Primary key
    log_id = Column(String(36), primary_key=True)
    
    # User reference
    telegram_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False, index=True)
    
    # Interaction data
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    technologies_identified = Column(JSON, nullable=True, default=list)
    
    # Metrics
    deepseek_tokens_used = Column(Integer, nullable=False, default=0)
    response_time_ms = Column(Integer, nullable=False)
    
    # Feedback
    user_feedback = Column(SQLEnum(FeedbackType), nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
