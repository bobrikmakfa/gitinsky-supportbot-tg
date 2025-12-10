"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import logging

from models import Base
from config import get_settings

logger = logging.getLogger(__name__)

# Database engine
engine = None
SessionLocal = None


def init_database():
    """Initialize database connection and create tables."""
    global engine, SessionLocal
    
    settings = get_settings()
    
    logger.info(f"Initializing database connection to: {settings.database_url}")
    
    # Create engine
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
        echo=settings.log_level == "DEBUG"
    )
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization complete")


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Get database session context manager."""
    if SessionLocal is None:
        init_database()
    
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """Get a new database session."""
    if SessionLocal is None:
        init_database()
    return SessionLocal()
