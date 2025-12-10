"""Main entry point for Gitinsky Support Bot."""

import logging
import sys
from pathlib import Path

from config import load_settings
from database import init_database
from bot import create_bot


def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=getattr(logging, log_level.upper()),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log')
        ]
    )


def main():
    """Main function to start the bot."""
    print("""
╔═══════════════════════════════════════╗
║   Gitinsky Support Bot                ║
║   Technical Support Assistant         ║
╚═══════════════════════════════════════╝
    """)
    
    try:
        # Load settings
        print("Loading configuration...")
        settings = load_settings()
        
        # Setup logging
        setup_logging(settings.log_level)
        logger = logging.getLogger(__name__)
        logger.info("Starting Gitinsky Support Bot...")
        
        # Initialize database
        print("Initializing database...")
        init_database()
        logger.info("Database initialized successfully")
        
        # Create and run bot
        print("Starting Telegram bot...")
        bot = create_bot()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\nShutting down bot...")
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
