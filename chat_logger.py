from datetime import datetime
from airtable_client import save_user_data

# Example chat log storage
chat_logs = []

def save_message(user_id, role, message):
    """
    Save a chat message to logs and export to Airtable.

    Args:
        user_id (str): The WhatsApp user ID.
        role (str): 'user' or 'assistant'.
        message (str): The message content.
    """
    timestamp = datetime.utcnow().isoformat()
    chat_logs.append({"timestamp": timestamp, "role": role, "message": message})
    print(f"Saved message: {message}")

    # Export to Airtable
    export_chat_to_airtable(user_id, [{"timestamp": timestamp, "role": role, "message": message}])