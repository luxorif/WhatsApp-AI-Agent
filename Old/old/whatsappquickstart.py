import json
import os
import requests
import aiohttp
import asyncio
from dotenv import load_dotenv


load_dotenv()
ACCESS_TOKEN = os.getenv("API_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")  # e.g., "120208836317406034@newsletter"

WHAPI_BASE_URL = "https://gate.whapi.cloud/messages/text"

# --------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------

def build_headers():
    """
    Build the headers required for Whapi requests.
    """
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

def build_text_message_input(recipient, message_body, typing_time=0):
    """
    Build the payload for sending a text message via Whapi.
    """
    return json.dumps(
        {
            "typing_time": typing_time,
            "to": recipient,
            "body": message_body,
        }
    )

# --------------------------------------------------------------
# Synchronous Message Sending
# --------------------------------------------------------------

def send_whatsapp_message_sync(recipient, message_body):
    """
    Send a synchronous WhatsApp text message via Whapi.
    """
    headers = build_headers()
    payload = build_text_message_input(recipient, message_body)

    try:
        response = requests.post(WHAPI_BASE_URL, headers=headers, data=payload)
        if response.status_code == 200:
            logging.info("Message sent successfully!")
            logging.info("Response:", response.json())
        else:
            logging.error(f"Failed to send message. Status: {response.status_code}")
            logging.error("Error:", response.text)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

# --------------------------------------------------------------
# Asynchronous Message Sending
# --------------------------------------------------------------

async def send_whatsapp_message_async(recipient, message_body):
    """
    Send an asynchronous WhatsApp text message via Whapi.
    """
    headers = build_headers()
    payload = build_text_message_input(recipient, message_body)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(WHAPI_BASE_URL, headers=headers, data=payload) as response:
                if response.status == 200:
                    logging.info("Message sent successfully!")
                    response_body = await response.json()
                    logging.info("Response:", response_body)
                else:
                    logging.error(f"Failed to send message. Status: {response.status}")
                    error_body = await response.text()
                    logging.error("Error:", error_body)
        except aiohttp.ClientConnectorError as e:
            logging.error("Connection Error:", str(e))

# --------------------------------------------------------------
# Execution
# --------------------------------------------------------------

if __name__ == "__main__":
    # Synchronous example
    logging.info("Sending synchronous message...")
    send_whatsapp_message_sync(RECIPIENT_WAID, "Hello, this is a test message.")

    # Asynchronous example
    logging.info("Sending asynchronous message...")
    asyncio.run(send_whatsapp_message_async(RECIPIENT_WAID, "Hello, this is an async test message."))