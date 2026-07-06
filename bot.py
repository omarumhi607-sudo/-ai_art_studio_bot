#!/usr/bin/env python
import logging
import sys
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from handlers import (
    start_command,
    help_command,
    about_command,
    generate_command,
    convert_command,
    shorten_command,
    button_callback,
    error_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot"""
    try:
        logger.info("Starting AI Art Studio Bot...")
        
        # Create application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("generate", generate_command))
        application.add_handler(CommandHandler("convert", convert_command))
        application.add_handler(CommandHandler("shorten", shorten_command))
        
        # Add callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("Bot is running! Press Ctrl+C to stop.")
        print("\n" + "="*50)
        print("🎨 AI Art Studio Bot is now running!")
        print(f"📱 Bot Username: @ai_art_studio_bot")
        print("="*50 + "\n")
        
        # Use run_polling with allowed updates
        application.run_polling(
            allowed_updates=None,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
