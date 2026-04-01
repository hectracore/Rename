from pyrogram import Client, filters
from pyrogram.raw.types import LabeledPrice
from config import Config
from database import db
from utils.log import get_logger

logger = get_logger("plugins.payments")

def is_public_mode():
    return Config.PUBLIC_MODE

@Client.on_callback_query(filters.regex(r"^buy_stars_(standard|deluxe)$"))
async def handle_buy_stars(client, callback_query):
    if not is_public_mode():
        return

    plan = callback_query.matches[0].group(1)
    user_id = callback_query.from_user.id

    config = await db.get_public_config()

    plan_key = f"premium_{plan}"
    plan_settings = config.get(plan_key, {})
    stars_price = plan_settings.get("stars_price", 0)

    if stars_price <= 0:
        await callback_query.answer("❌ Stars payment is not configured for this plan.", show_alert=True)
        return

    title = f"Premium {plan.capitalize()} Plan"
    description = f"Purchase the Premium {plan.capitalize()} Plan via Telegram Stars. You will enjoy enhanced limits and features."
    payload = f"buy_premium_{plan}_{user_id}"
    currency = "XTR"

    # In Pyrogram v2, we must use the raw `SendInvoice` method for sending invoices,
    # or the raw Invoice object. Wait, Pyrogram does not have a native `send_invoice` wrapper
    # unless it was added later. Let's use the raw API method just to be completely safe.

    try:
        from pyrogram.raw.functions.messages import SendMedia
        from pyrogram.raw.types import InputMediaInvoice, Invoice, InputPeerUser, DataJSON
        import json

        peer = await client.resolve_peer(user_id)

        invoice = Invoice(
            test=False,
            name_requested=False,
            phone_requested=False,
            email_requested=False,
            shipping_address_requested=False,
            flexible=False,
            phone_to_provider=False,
            email_to_provider=False,
            currency=currency,
            prices=[LabeledPrice(label=title, amount=stars_price)]
        )

        input_media = InputMediaInvoice(
            title=title,
            description=description,
            invoice=invoice,
            payload=payload.encode('utf-8'),
            provider="",
            provider_data=DataJSON(data="{}")
        )

        from pyrogram.raw.functions.messages import SendMedia
        await client.invoke(
            SendMedia(
                peer=peer,
                media=input_media,
                message="",
                random_id=client.rnd_id()
            )
        )
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Failed to send invoice: {e}")
        await callback_query.answer(f"❌ Error generating invoice.", show_alert=True)

@Client.on_raw_update(group=-2)
async def raw_update_handler(client, update, users, chats):
    from pyrogram.raw.types import UpdateBotPrecheckoutQuery, UpdateMessageID

    if isinstance(update, UpdateBotPrecheckoutQuery):
        try:
            from pyrogram.raw.functions.messages import SetBotPrecheckoutResults

            await client.invoke(
                SetBotPrecheckoutResults(
                    query_id=update.query_id,
                    success=True
                )
            )
            logger.info(f"Successfully answered pre-checkout query for {update.user_id}")
        except Exception as e:
            logger.error(f"Failed to answer pre-checkout query: {e}")

@Client.on_message(filters.service & filters.private)
async def handle_successful_payment(client, message):
    if not is_public_mode():
        return

    # In Pyrogram v2, the Action object may contain the payment info, or it may be raw.
    # The `message.action` type could be `MessageActionPaymentSuccessfulMe` or similar.
    # Since Pyrogram doesn't have a cleanly parsed `successful_payment` object in the standard Message,
    # we inspect the raw message action or text if possible.

    action = getattr(message, "action", None)

    # We can also check raw if the action doesn't map directly
    is_payment = False
    payload = ""
    amount = 0

    if hasattr(message, "action") and message.action:
        # Check action string representations
        if "Payment" in str(message.action) or "payment" in str(message.action):
            is_payment = True

    # Alternatively, Pyrogram may attach it to message.successful_payment directly in some patches
    # or the raw type is accessible via message.service.

    # Actually, a safer approach to catch the payment is to parse the `MessageActionPaymentSuccessful`
    # from the raw message if it exists.

    if getattr(message, "successful_payment", None):
        is_payment = True
        payment_info = message.successful_payment
        payload = getattr(payment_info, "invoice_payload", "")
        amount = getattr(payment_info, "total_amount", 0)
    elif getattr(message, "_client", None):
        # Dig into raw pyrogram message to find payment
        raw_msg = message
        if hasattr(raw_msg, "action") and raw_msg.action:
            action_type = type(raw_msg.action).__name__
            if "PaymentSuccessful" in action_type:
                is_payment = True
                payload = getattr(raw_msg.action, "invoice_payload", b"").decode('utf-8', errors='ignore')
                amount = getattr(raw_msg.action, "total_amount", 0)

    if is_payment and payload:
        if payload.startswith("buy_premium_"):
            parts = payload.split("_")
            if len(parts) >= 4:
                plan = parts[2]
                target_user_id = int(parts[3])

                # Default hardcoded period is 30 days
                # Add 30 days for Stars payment
                await db.add_premium_user(target_user_id, days=30, plan=plan)

                await message.reply_text(
                    f"✅ **Payment Successful!**\n\n"
                    f"Thank you for purchasing the **Premium {plan.capitalize()} Plan**.\n\n"
                    f"Your account has been upgraded for 30 days. Enjoy!"
                )

                await db.add_log("stars_payment", Config.CEO_ID, f"User {target_user_id} paid for {plan} plan")
