from pyrogram import Client, idle
from config import Config
from utils.log import get_logger

# Configure logging
logger = get_logger("main")

# Initialize Bot
app = Client(
    "xtv_rename_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    if not Config.BOT_TOKEN:
        logger.error("BOT_TOKEN is not set!")
        exit(1)

    logger.info("Starting XTV Rename Bot...")
    app.start()
    logger.info("Bot Started!")
    idle()
    app.stop()
