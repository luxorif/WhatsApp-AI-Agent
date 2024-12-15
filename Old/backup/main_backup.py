from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
import openai

# Load environment variables
load_dotenv()
api_token = os.getenv("API_TOKEN")
url = os.getenv("SEND_MESSAGE_URL")  # URL for sending text messages
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Root route to respond to GET requests
@app.route('/')
def home():
    return jsonify({"message": "Webhook App is Running!"}), 200

# Webhook route to handle POST requests
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Get the incoming JSON data
    data = request.json
    print(f"Data received: {data}")

    # Check if 'messages' exist in the data
    if data and 'messages' in data:
        for message in data['messages']:
            # Ignore messages sent by yourself (to prevent an infinite loop)
            if message.get('from_me', False):
                print("Ignoring message from myself.")
                continue

            # Process incoming messages
            chat_id = message.get('chat_id')  # Extract the chat ID
            text = message.get('text', {}).get('body', '')  # Extract the message text
            print(f"Message from {chat_id}: {text}")

            # Send an auto-reply
            send_auto_reply(chat_id, f"Received your message: {text}")
    else:
        print("No 'messages' field in the incoming data.")

    return jsonify({"status": "success"}), 200


def send_auto_reply(chat_id, text):
    payload = {
        "to": chat_id,
        "body": text,
    }
    headers = {
        "authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    try:
        # Send the message
        response = requests.post(url, json=payload, headers=headers)
        print(f"Auto-reply status: {response.status_code}, response: {response.text}")
    except Exception as e:
        print(f"Failed to send auto-reply: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)