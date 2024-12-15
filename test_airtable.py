import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable configuration
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

def test_airtable_connection():
    """
    Test Airtable connection by saving a test record.
    """
    base_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }
    record = {
        "fields": {
            "User_ID": "test_user",
            "Message Content": "This is a test message to verify Airtable connection."
        }
    }
    try:
        response = requests.post(base_url, json=record, headers=headers)
        response.raise_for_status()
        print("Record saved successfully:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error saving record to Airtable:", e)

if __name__ == "__main__":
    test_airtable_connection()