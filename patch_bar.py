with open("plugins/public_cmds.py", "r") as f:
    content = f.read()

bad_str = '''    # 10 blocks total
    filled_blocks = int(max_percent / 10)
    empty_blocks = 10 - filled_blocks'''

good_str = '''    # 12 blocks total
    filled_blocks = int((max_percent / 100) * 12)
    empty_blocks = 12 - filled_blocks'''

content = content.replace(bad_str, good_str)

with open("plugins/public_cmds.py", "w") as f:
    f.write(content)
