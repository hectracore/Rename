from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from database import db
from plugins.admin import admin_sessions, is_admin
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.log import get_logger

logger = get_logger("plugins.force_sub_handler")


@Client.on_chat_member_updated(filters.channel)
async def handle_bot_added_to_channel(client, update):
    if not Config.PUBLIC_MODE:
        return

    user_id = update.from_user.id

    if not is_admin(user_id):
        return

    state = admin_sessions.get(user_id)
    if state not in ["awaiting_public_force_sub", "awaiting_fs_add_channel"] and not (isinstance(state, str) and state.startswith("awaiting_force_sub_channel_")):
        return

    new_status = update.new_chat_member.status if update.new_chat_member else None

    if new_status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        chat_id = update.chat.id
        chat_title = update.chat.title

        try:
            chat_info = await client.get_chat(chat_id)
            invite_link = chat_info.invite_link
            if not invite_link:
                invite_link = await client.export_chat_invite_link(chat_id)

            username = chat_info.username

            if state == "awaiting_public_force_sub":
                # Legacy single-channel
                await db.update_public_config("force_sub_channel", chat_id)
                await db.update_public_config("force_sub_link", invite_link)
                await db.update_public_config("force_sub_username", username)

                await client.send_message(
                    chat_id=user_id,
                    text=f"✅ **Force-Sub Setup Complete!**\n\nI successfully detected that you added me to **{chat_title}**.\n\nChannel ID: `{chat_id}`\nSaved Link: {invite_link}",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🔙 Back to Menu", callback_data="admin_main"
                                )
                            ]
                        ]
                    ),
                )
                admin_sessions.pop(user_id, None)
            else:
                # Multi-channel setup
                config = await db.get_public_config()
                channels = config.get("force_sub_channels", [])

                new_channel = {
                    "id": chat_id,
                    "link": invite_link,
                    "username": username,
                    "title": chat_title,
                    "button_label": f"📢 Join {chat_title}"
                }

                channels.append(new_channel)
                await db.update_public_config("force_sub_channels", channels)

                # Keep legacy field populated for backward compat if it's the first channel
                if len(channels) == 1:
                    await db.update_public_config("force_sub_channel", chat_id)
                    await db.update_public_config("force_sub_link", invite_link)
                    await db.update_public_config("force_sub_username", username)

                await client.send_message(
                    chat_id=user_id,
                    text=f"✅ **Force-Sub Channel Added!**\n\nI successfully detected that you added me to **{chat_title}**.\n\nChannel ID: `{chat_id}`\nSaved Link: {invite_link}",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🔙 Back to Config", callback_data="admin_force_sub_menu"
                                )
                            ]
                        ]
                    ),
                )
                admin_sessions.pop(user_id, None)


        except Exception as e:
            logger.error(f"Force sub setup error during chat_member_updated: {e}")
            await client.send_message(
                chat_id=user_id,
                text=f"❌ **Failed to verify channel.**\n\nI was added to the channel, but I don't have permission to create invite links. Please grant me the 'Invite Users via Link' permission.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("❌ Cancel", callback_data="admin_force_sub_menu")]]
                ),
            )


# --------------------------------------------------------------------------
# Developed by 𝕏0L0™ (@davdxpx) | © 2026 XTV Network Global
# Don't Remove Credit
# Telegram Channel @XTVbots
# Developed for the 𝕏TV Network @XTVglobal
# Backup Channel @XTVhome
# Contact on Telegram @davdxpx
# --------------------------------------------------------------------------
