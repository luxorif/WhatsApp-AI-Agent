from flask import jsonify
from openai_client import openai_client  # Import the OpenAIClient instance
import requests
import config
import logging

def send_auto_reply(chat_id, text):
    """
    Sends an auto-reply message to a specified WhatsApp chat.
    """
    payload = {"to": chat_id, "body": text}
    headers = {
        "authorization": f"Bearer {config.API_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(config.SEND_MESSAGE_URL, json=payload, headers=headers)
        logging.info(f"Auto-reply status: {response.status_code}, response: {response.text}")
    except Exception as e:
        logging.error(f"Failed to send auto-reply: {e}")

def handle_whatsapp_message(data):
    """
    Processes incoming WhatsApp messages, fetches a reply from OpenAI, 
    and sends the response back to the user.
    """
    messages = data.get("messages", [])
    for message in messages:
        if message.get("from_me", False):
            continue  # Skip messages sent by the bot

        # Extract user message and chat ID
        chat_id = message.get("chat_id")
        user_message = message.get("text", {}).get("body", "")
        logging.info(f"Received message from {chat_id}: {user_message}")

        # Get assistant's reply
        assistant_reply = openai_client.get_reply(chat_id, user_message)
        logging.info(f"Assistant reply for {chat_id}: {assistant_reply}")

        # Send the assistant's reply back to WhatsApp
        send_auto_reply(chat_id, assistant_reply)

    return jsonify({"status": "success"}), 200