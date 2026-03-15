import re

with open("database.py", "r") as f:
    content = f.read()

bad_str = '''            # Check limits
            if daily_file_count_limit > 0 and usage.get("file_count", 0) >= daily_file_count_limit:
                await self.record_quota_hit(user_id)
                return False, f"You've reached your daily {daily_file_count_limit} file limit.", usage

            if daily_egress_mb_limit > 0 and (usage.get("egress_mb", 0.0) + incoming_mb) > daily_egress_mb_limit:
                await self.record_quota_hit(user_id)
                mb_limit_str = f"{daily_egress_mb_limit} MB"
                if daily_egress_mb_limit >= 1024:
                    mb_limit_str = f"{daily_egress_mb_limit / 1024:.2f} GB"
                return False, f"You've reached your daily {mb_limit_str} egress limit.", usage

            return True, "", usage'''

good_str = '''            # Calculate time to midnight
            current_utc = datetime.datetime.utcnow()
            tomorrow = current_utc + datetime.timedelta(days=1)
            midnight = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
            time_to_midnight = midnight - current_utc
            hours, remainder = divmod(int(time_to_midnight.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            reset_str = f"Resets at midnight UTC — roughly {hours}h {minutes}m from now."

            # Check limits
            if daily_file_count_limit > 0 and usage.get("file_count", 0) >= daily_file_count_limit:
                await self.record_quota_hit(user_id)
                return False, f"You've reached your daily {daily_file_count_limit} file limit. {reset_str}", usage

            if daily_egress_mb_limit > 0 and (usage.get("egress_mb", 0.0) + incoming_mb) > daily_egress_mb_limit:
                await self.record_quota_hit(user_id)
                mb_limit_str = f"{daily_egress_mb_limit} MB"
                if daily_egress_mb_limit >= 1024:
                    mb_limit_str = f"{daily_egress_mb_limit / 1024:.2f} GB"
                return False, f"You've reached your daily {mb_limit_str} egress limit. {reset_str}", usage

            return True, "", usage'''

content = content.replace(bad_str, good_str)

with open("database.py", "w") as f:
    f.write(content)
