import re
with open("plugins/process.py", "r") as f:
    content = f.read()

bad_str = '''async def process_file(client, message, data):
    processor = TaskProcessor(client, message, data)
    await processor.run()'''

good_str = '''async def process_file(client, message, data):
    file_msg = data.get("file_message")
    user_id = file_msg.from_user.id if file_msg else (message.from_user.id if message else None)

    if user_id:
        # Before we actually spawn the task, do the quota check!
        file_size = 0
        if file_msg:
            media = file_msg.document or file_msg.video
            if media:
                file_size = media.file_size

        # Check quota
        quota_ok, error_msg, _ = await db.check_daily_quota(user_id, file_size)
        if not quota_ok:
            if message:
                await message.edit_text(f"🛑 **Quota Exceeded**\\n\\n{error_msg}")
            return

    processor = TaskProcessor(client, message, data)
    await processor.run()'''

content = content.replace(bad_str, good_str)

with open("plugins/process.py", "w") as f:
    f.write(content)
