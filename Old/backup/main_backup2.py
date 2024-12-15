from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import time
from time import sleep

# Load environment variables
load_dotenv()
api_token = os.getenv("API_TOKEN")
url = os.getenv("SEND_MESSAGE_URL")
openai_api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_fllCyHROOJfQNiSIMuR5gzRZ"

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Flask app initialization
app = Flask(__name__)

# Function to get assistant's reply using thread and run logic
def get_openai_reply(message_text):
    try:
        print(f"Asking the assistant: {message_text}")

        # Step 1: Create a thread
        thread = client.beta.threads.create()

        # Step 2: Add user message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_text
        )

        # Step 3: Start the assistant run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Step 4: Wait for the assistant's response
        while not run.status == "completed":
            print("Waiting for assistant's response...")
            sleep(2)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Step 5: Retrieve the final response
        messages = client.beta.threads.messages.list(thread.id)
        try:
            assistant_reply = messages.data[0].content[0].text.value
            print(f"Assistant Reply: {assistant_reply}")
            return assistant_reply
        except Exception as e:
            print(f"Error extracting assistant reply: {e}")
            return "Sorry, something went wrong."

    except Exception as e:
        print(f"Error connecting to OpenAI Assistant: {e}")
        return "Sorry, something went wrong."

# Function to send an auto-reply via WhatsApp
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

# Webhook handler for incoming WhatsApp messages
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    if data and 'messages' in data:
        for message in data['messages']:
            # Ignore messages sent by the bot itself
            if message.get('from_me', False):
                continue

            # Extract user message and chat ID
            chat_id = message.get('chat_id')
            user_message = message.get('text', {}).get('body', '')
            print(f"User message: {user_message}")

            # Get the assistant's reply
            assistant_reply = get_openai_reply(user_message)
            print(f"Assistant Reply: {assistant_reply}")

            # Send the reply back to the user
            send_auto_reply(chat_id, assistant_reply)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)