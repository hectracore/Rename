import re
with open("plugins/flow.py", "r") as f:
    content = f.read()

bad_str = '''    if media:
        file_size = media.file_size

        # Check daily quota
        quota_ok, error_msg, _ = await db.check_daily_quota(user_id, file_size)
        if not quota_ok:
            await message.reply_text(f"🛑 **Quota Exceeded**\\n\\n{error_msg}")
            return

        if file_size > 4000 * 1024 * 1024:'''

good_str = '''    if media:
        file_size = media.file_size

        # WE MOVED QUOTA CHECK OUT OF HERE AND INTO process_file()

        if file_size > 4000 * 1024 * 1024:'''

content = content.replace(bad_str, good_str)

with open("plugins/flow.py", "w") as f:
    f.write(content)
