import io
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import *
from utils import generate_image, shorten_url, convert_image, is_valid_image_format, validate_url

logger = logging.getLogger(__name__)

# ============= START COMMAND =============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with welcome message and inline keyboard"""
    user = update.effective_user
    first_name = user.first_name or "User"
    
    welcome_text = f"""
🎨 **Welcome to AI Art Studio Bot!**

Hello {first_name}! 👋

I'm your all-in-one creative assistant. Here's what I can do for you:

**🎨 Generate AI Art**
Transform your imagination into stunning images using AI
→ `/generate a sunset over mountains`

**🔄 Convert Images**
Change image formats instantly
→ Reply to an image with `/convert png`

**🔗 Shorten URLs**
Make long links short and shareable
→ `/shorten https://example.com/long-url`

**✨ Features:**
• Free and unlimited usage
• High-quality image generation
• Supports multiple image formats
• No registration required

Ready to create something amazing? Just type a command or click a button below!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🎨 Generate Art", callback_data='quick_generate'),
            InlineKeyboardButton("🔄 Convert Image", callback_data='quick_convert')
        ],
        [
            InlineKeyboardButton("🔗 Shorten URL", callback_data='quick_shorten'),
            InlineKeyboardButton("❓ Help", callback_data='quick_help')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

# ============= HELP COMMAND =============

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = f"""
📚 **Help - {BOT_NAME}**

**Available Commands:**

/start - 🚀 Welcome message and quick actions
/generate [prompt] - 🎨 Create AI art from text
/convert [format] - 🔄 Convert image format (reply to image)
/shorten [url] - 🔗 Shorten a long URL
/help - ❓ Show this help message
/about - ℹ️ About this bot

**Detailed Usage:**

**1. Generate AI Art**
