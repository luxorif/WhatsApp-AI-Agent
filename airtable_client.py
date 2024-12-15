import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable environment variables
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")


class AirtableClient:
    def __init__(self, base_id, table_name, api_key):
        self.base_id = base_id
        self.table_name = table_name
        self.api_key = api_key
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def save_record(self, user_id, message_content):
        """
        Save a single record to Airtable.
        :param user_id: User ID (e.g., WhatsApp number).
        :param message_content: The message content to store.
        :return: API response or None in case of failure.
        """
        record = {
            "fields": {
                "User_ID": user_id,
                "Message Content": message_content,
            }
        }

        try:
            response = requests.post(self.base_url, json=record, headers=self.headers)
            response.raise_for_status()
            print(f"Record saved successfully: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error saving record to Airtable: {e}")
            return None


# Initialize the Airtable client
airtable_client = AirtableClient(
    base_id=AIRTABLE_BASE_ID,
    table_name=AIRTABLE_TABLE_NAME,
    api_key=AIRTABLE_API_KEY,
)