import os
import json
import logging
import uuid
from datetime import datetime
from typing import List, Dict

# ------------------------------------------
# Logger Setup (logs/app.log)
# ------------------------------------------
logger = logging.getLogger("optimizer")
logger.setLevel(logging.INFO)
os.makedirs("logs", exist_ok=True)

log_file_path = os.path.join("logs", "app.log")
if not logger.handlers:
    handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ------------------------------------------
# Input Validation
# ------------------------------------------
def validate_input(data: Dict) -> str:
    if "budget" not in data or not isinstance(data["budget"], int) or data["budget"] <= 0:
        return "Budget must be a positive integer."
    
    if "items" not in data or not isinstance(data["items"], list) or len(data["items"]) == 0:
        return "Items must be a non-empty list."

    for i, item in enumerate(data["items"]):
        if not all(k in item for k in ("name", "price", "value")):
            return f"Item {i + 1} is missing required fields (name, price, value)."

        if not isinstance(item["name"], str) or not item["name"].strip():
            return f"Item {i + 1} has an invalid or empty name."

        if not isinstance(item["price"], int) or item["price"] <= 0:
            return f"Item '{item.get('name', '?')}' has an invalid price (must be a positive integer)."

        if not isinstance(item["value"], int) or item["value"] <= 0:
            return f"Item '{item.get('name', '?')}' has an invalid value (must be a positive integer)."

    return ""  # No error

# ------------------------------------------
# Unique Session ID Generator
# ------------------------------------------
def generate_session_id() -> str:
    return str(uuid.uuid4())[:8]  # Shortened for simplicity

# ------------------------------------------
# Save Session Result (daily folder + history.json)
# ------------------------------------------
def save_session_result(session_id: str, result: Dict):
    # Save to logs/YYYY-MM-DD/session_<id>.json
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join("logs", date_str)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"session_{session_id}.json")
    with open(file_path, "w") as f:
        json.dump(result, f, indent=2)

    logger.info(f"Session {session_id} saved to {file_path}")

    # Append to history file
    append_to_history(result)

# ------------------------------------------
# History File Handling
# ------------------------------------------
HISTORY_FILE = os.path.join("logs", "history.json")

def append_to_history(session_data: Dict, user_id: str = "guest_user"):
    os.makedirs("logs", exist_ok=True)
    
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = {}

    history.setdefault(user_id, [])
    history[user_id].append(session_data)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def get_history(user_id: str = "guest_user") -> List[Dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    return history.get(user_id, [])
