import re

with open("plugins/admin.py", "r") as f:
    content = f.read()

bad_str = '''    except Exception:
        name = "Unknown User"
        username = "N/A"

    text = (
        f"👤 **User Lookup**\\n\\n"
        f"**ID:** `{user_id}`\\n"
        f"**Name:** {name}\\n"
        f"**Username:** {username}\\n"'''

good_str = '''    except Exception:
        name = "Unknown User"
        username = "N/A"

    user_settings = await db.get_settings(user_id)
    joined_date = "Unknown"

    # Check if there is a document at all
    has_thumb = "No"
    current_template = "Default"

    if user_settings:
        if user_settings.get("thumbnail_file_id") or user_settings.get("thumbnail_binary"):
            has_thumb = "Yes"

        templates = user_settings.get("templates", {})
        if templates and templates.get("caption") != "{random}":
            current_template = "Custom"

        # Try to extract joined date from ObjectID if available, else from usage.date
        _id = user_settings.get("_id")
        if _id:
            try:
                # ObjectId contains a timestamp
                import bson
                if isinstance(_id, bson.ObjectId):
                    joined_date = _id.generation_time.strftime("%d %b %Y")
                else:
                    joined_date = usage.get("date", "Unknown")
            except Exception:
                joined_date = usage.get("date", "Unknown")

    text = (
        f"👤 **User Lookup**\\n\\n"
        f"**ID:** `{user_id}`\\n"
        f"**Name:** {name}\\n"
        f"**Username:** {username}\\n"
        f"**Joined:** {joined_date}\\n"
        f"**Template:** {current_template}\\n"
        f"**Custom Thumb:** {has_thumb}\\n"'''

content = content.replace(bad_str, good_str)

with open("plugins/admin.py", "w") as f:
    f.write(content)
