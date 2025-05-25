# logger.py
import os
from datetime import datetime

LOG_FILE = "unknown_commands.log"

def log_unknown_command(user_id: int, username: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {username} ({user_id}): {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line)