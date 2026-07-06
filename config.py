import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables")

# API Endpoints
POLLINATIONS_API = "https://image.pollinations.ai/prompt/"
URL_SHORTENER_API = "https://spoo.me/"

# Supported image formats for conversion
SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp', 'tiff']

# Image generation settings
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024

# Bot information
BOT_NAME = "AI Art Studio Bot"
BOT_USERNAME = "ai_art_studio_bot"
BOT_VERSION = "1.0.0"

# Command descriptions for help menu
COMMAND_DESCRIPTIONS = {
    'start': '🚀 Start the bot and see welcome message',
    'generate': '🎨 Generate an AI image from text prompt',
    'convert': '🔄 Convert an image to different format',
    'shorten': '🔗 Shorten a long URL',
    'help': '❓ Show all available commands',
    'about': 'ℹ️ About this bot'
}
