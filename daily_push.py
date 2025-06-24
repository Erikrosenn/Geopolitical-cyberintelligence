import os
import shutil
import subprocess
from datetime import datetime

# 1. Define today's date and folder
today = datetime.now().strftime("%Y-%m-%d")
folder_name = today  # This will be created by scraper.py

# 2. Clean repo except key files
for item in os.listdir():
    if item not in ("README.md", ".git", "daily_push.py", "scraper.py"):
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

# 3. Run scraper.py to generate today's folder
subprocess.run(["python", "scraper.py"], check=True)

# 4. Git operations
subprocess.run(["git", "add", folder_name], check=True)
subprocess.run(["git", "commit", "-m", f"🗞️ Add daily report for {today}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
