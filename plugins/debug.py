from pyrogram import Client, filters
from utils.log import get_logger

logger = get_logger("plugins.debug")

@Client.on_message(filters.all, group=-1)
async def debug_all_messages(client, message):
    sender_id = message.from_user.id if message.from_user else (message.sender_chat.id if message.sender_chat else "Unknown")
    logger.info(f"Received message from {sender_id}: {message.text or message.caption or '[Media]'}")
