from pyrogram import Client, filters
from utils.log import get_logger

logger = get_logger("plugins.debug")

@Client.on_message(filters.all, group=-1)
async def debug_all_messages(client, message):
    logger.info(f"Received message from {message.from_user.id}: {message.text or message.caption or '[Media]'}")
