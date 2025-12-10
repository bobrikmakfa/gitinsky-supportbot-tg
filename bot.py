"""Telegram bot handler with command processing."""

import logging
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram.constants import ParseMode

from config import get_settings
from auth import get_auth_service
from query_processor import get_query_processor
from knowledge_base import get_kb_manager
from models import TechnologyCategory, FeedbackType, InteractionLog
from database import get_db

logger = logging.getLogger(__name__)

# Conversation states
AWAITING_EMAIL, AWAITING_CODE, AWAITING_FEEDBACK = range(3)


class TelegramBot:
    """Telegram bot handler."""
    
    def __init__(self):
        """Initialize bot handler."""
        self.settings = get_settings()
        self.auth_service = get_auth_service()
        self.query_processor = get_query_processor()
        self.kb_manager = get_kb_manager()
        self.application = None
        
        # Store pending feedback log IDs
        self.pending_feedback: Dict[int, str] = {}
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user
        telegram_id = user.id
        
        welcome_message = f"""👋 Welcome to **Gitinsky Support Bot**!

I'm here to help you with technical questions about the technologies we use in our projects.

**Supported Technologies:**
🔹 Orchestration: Ansible, Kubernetes, OpenShift, Puppet
🔹 Containers: Docker, Docker Swarm, Docker Compose
🔹 IaC: Terraform
🔹 CI/CD: Argo CD, GitLab CI
🔹 Monitoring: ELK, Zabbix, Grafana, Prometheus
🔹 Databases: MySQL, PostgreSQL
🔹 Networking: Cisco, Mikrotik, Keenetic
🔹 OS: Linux, Windows Administration
🔹 Programming: Python
🔹 System Administration

"""
        
        if self.auth_service.check_user_verified(telegram_id):
            welcome_message += "✅ You're verified! Just send me your technical questions.\n\nUse /help to see all available commands."
        else:
            welcome_message += "⚠️ You need to verify your company email first.\n\nUse /verify to start the verification process."
        
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        telegram_id = update.effective_user.id
        
        if not self.auth_service.check_user_verified(telegram_id):
            await update.message.reply_text(
                "⚠️ Please verify your email first using /verify"
            )
            return
        
        help_text = """📖 **Available Commands:**

/start - Start the bot and see welcome message
/help - Display this help message
/status - Check your verification status
/verify - Start email verification process
/feedback - Rate the last response

**How to use:**
Just send me your technical question, and I'll help you based on our company's knowledge base and best practices.

**Example questions:**
• "How do I deploy an app with Kubernetes?"
• "What's the best way to write an Ansible playbook?"
• "How to troubleshoot Docker container issues?"

Need help? Contact your team lead or system administrator.
"""
        
        if self.auth_service.is_admin(telegram_id):
            help_text += "\n**Admin Commands:**\n/admin_list_users - List all verified users"
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        telegram_id = update.effective_user.id
        exists, status_message = self.auth_service.get_user_status(telegram_id)
        
        await update.message.reply_text(
            f"**Your Status:**\n\n{status_message}",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def verify_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /verify command - start verification."""
        await update.message.reply_text(
            f"📧 **Email Verification**\n\n"
            f"Please send me your company email address (must be from @{self.settings.company_email_domain}):"
        )
        return AWAITING_EMAIL
    
    async def verify_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle email input during verification."""
        user = update.effective_user
        email = update.message.text.strip()
        
        success, message = await self.auth_service.start_verification(
            telegram_id=user.id,
            username=user.username,
            email=email
        )
        
        if success:
            await update.message.reply_text(
                f"✅ {message}\n\n"
                f"Please check your email and enter the verification code:"
            )
            return AWAITING_CODE
        else:
            await update.message.reply_text(
                f"❌ {message}\n\n"
                f"Please try again with a valid company email:"
            )
            return AWAITING_EMAIL
    
    async def verify_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle verification code input."""
        telegram_id = update.effective_user.id
        code = update.message.text.strip()
        
        success, message = self.auth_service.verify_code(telegram_id, code)
        
        await update.message.reply_text(message)
        
        if success:
            return ConversationHandler.END
        else:
            await update.message.reply_text("Please enter the correct code or use /verify to get a new one:")
            return AWAITING_CODE
    
    async def verify_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel verification process."""
        await update.message.reply_text(
            "❌ Verification cancelled. Use /verify to start again."
        )
        return ConversationHandler.END
    
    async def feedback_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /feedback command."""
        telegram_id = update.effective_user.id
        
        if not self.auth_service.check_user_verified(telegram_id):
            await update.message.reply_text("⚠️ Please verify your email first using /verify")
            return
        
        # Get last interaction
        try:
            with get_db() as db:
                last_log = db.query(InteractionLog).filter(
                    InteractionLog.telegram_id == telegram_id,
                    InteractionLog.user_feedback == None
                ).order_by(InteractionLog.timestamp.desc()).first()
                
                if not last_log:
                    await update.message.reply_text("No recent responses to rate.")
                    return
                
                # Create feedback keyboard
                keyboard = [
                    [
                        InlineKeyboardButton("👍 Helpful", callback_data=f"feedback_helpful_{last_log.log_id}"),
                        InlineKeyboardButton("👎 Not Helpful", callback_data=f"feedback_not_helpful_{last_log.log_id}")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    "How would you rate the last response?",
                    reply_markup=reply_markup
                )
        except Exception as e:
            logger.error(f"Error in feedback command: {e}")
            await update.message.reply_text("Error retrieving feedback options.")
    
    async def feedback_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle feedback button clicks."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        if data.startswith("feedback_"):
            parts = data.split("_")
            feedback_value = parts[1]  # helpful or not_helpful
            log_id = "_".join(parts[2:])
            
            try:
                with get_db() as db:
                    log_entry = db.query(InteractionLog).filter(
                        InteractionLog.log_id == log_id
                    ).first()
                    
                    if log_entry:
                        log_entry.user_feedback = FeedbackType.HELPFUL if feedback_value == "helpful" else FeedbackType.NOT_HELPFUL
                        db.commit()
                        
                        await query.edit_message_text(
                            f"✅ Thank you for your feedback! ({feedback_value.replace('_', ' ')})"
                        )
                    else:
                        await query.edit_message_text("Error: Feedback entry not found.")
            except Exception as e:
                logger.error(f"Error saving feedback: {e}")
                await query.edit_message_text("Error saving feedback.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages (technical questions)."""
        user = update.effective_user
        telegram_id = user.id
        message_text = update.message.text
        
        # Check if user is verified
        if not self.auth_service.check_user_verified(telegram_id):
            await update.message.reply_text(
                "⚠️ You need to verify your company email first.\n\nUse /verify to start the verification process."
            )
            return
        
        # Update last interaction
        self.auth_service.update_last_interaction(telegram_id)
        
        # Send typing indicator
        await update.message.chat.send_action("typing")
        
        # Process query
        try:
            result = await self.query_processor.process_query(telegram_id, message_text)
            
            if result['success']:
                response = result['response']
                
                # Send response (split if too long)
                if len(response) > 4000:
                    # Split into chunks
                    chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                    for chunk in chunks:
                        await update.message.reply_text(chunk)
                else:
                    await update.message.reply_text(response)
                
                # Add feedback buttons if enabled
                if self.settings.enable_feedback_collection:
                    # The log_id is stored in the database, we need to get it
                    # For simplicity, we'll add feedback option via /feedback command
                    pass
            else:
                await update.message.reply_text(
                    "Sorry, I encountered an error processing your request. Please try again."
                )
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(
                "An error occurred while processing your request. Please try again later."
            )
    
    async def admin_list_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin command: List all verified users."""
        telegram_id = update.effective_user.id
        
        if not self.auth_service.is_admin(telegram_id):
            await update.message.reply_text("⚠️ This command is only available to administrators.")
            return
        
        try:
            from models import User, VerificationStatus
            with get_db() as db:
                users = db.query(User).filter(
                    User.verification_status == VerificationStatus.VERIFIED
                ).all()
                
                if not users:
                    await update.message.reply_text("No verified users found.")
                    return
                
                user_list = "**Verified Users:**\n\n"
                for user in users:
                    user_list += f"• {user.email} (ID: {user.telegram_id})\n"
                    user_list += f"  Verified: {user.verified_at.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
                
                await update.message.reply_text(user_list, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            await update.message.reply_text("Error retrieving user list.")
    
    def setup_handlers(self):
        """Set up bot command and message handlers."""
        # Verification conversation handler
        verify_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("verify", self.verify_start)],
            states={
                AWAITING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.verify_email)],
                AWAITING_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.verify_code)],
            },
            fallbacks=[CommandHandler("cancel", self.verify_cancel)],
        )
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(verify_conv_handler)
        self.application.add_handler(CommandHandler("feedback", self.feedback_command))
        self.application.add_handler(CallbackQueryHandler(self.feedback_callback, pattern="^feedback_"))
        
        # Admin commands
        if self.settings.enable_admin_commands:
            self.application.add_handler(CommandHandler("admin_list_users", self.admin_list_users))
        
        # Message handler (for technical questions)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    def run(self):
        """Start the bot."""
        logger.info("Starting Telegram bot...")
        
        # Create application
        self.application = Application.builder().token(self.settings.telegram_bot_token).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Run bot
        logger.info("Bot is running. Press Ctrl+C to stop.")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def create_bot() -> TelegramBot:
    """Create and return bot instance."""
    return TelegramBot()
