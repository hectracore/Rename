from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from utils.log import get_logger

# Setup logger
logger = get_logger("plugins.start")
logger.info("Loading plugins.start...")

# Use group=1 to match flow.py and ensure visibility
@Client.on_message(filters.command(["start", "new"]) & filters.private, group=1)
async def handle_start_command_unique(client, message):
    user_id = message.from_user.id
    logger.info(f"CMD received: {message.text} from {user_id}")

    if not (user_id == Config.CEO_ID or user_id in Config.FRANCHISEE_IDS):
        logger.warning(f"Unauthorized access by {user_id}")
        return

    await message.reply_text(
        "**XTV Rename Bot**\n\n"
        "Welcome to the official XTV file renaming tool.\n"
        "This bot provides professional renaming and metadata management.\n\n"
        "Click below to start.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Start Renaming", callback_data="start_renaming")]
        ])
    )

@Client.on_message(filters.command("end") & filters.private, group=1)
async def handle_end_command_unique(client, message):
    user_id = message.from_user.id
    logger.info(f"CMD received: {message.text} from {user_id}")
    await message.reply_text("Session ended. Use /start or /new to begin again.")
