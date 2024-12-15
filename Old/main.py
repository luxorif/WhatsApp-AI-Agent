from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests  # Import the requests module
from time import sleep

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
api_token = os.getenv("API_TOKEN")
send_message_url = os.getenv("SEND_MESSAGE_URL")
ASSISTANT_ID = "asst_DrxHBTeJ1ECjLSswtwSemD0M"

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Flask app initialization
app = Flask(__name__)

# Global dictionary to track threads for users
user_threads = {}
user_message_index = {}

# Function to send an auto-reply via WhatsApp
def send_auto_reply(chat_id, text):
    payload = {"to": chat_id, "body": text}
    headers = {
        "authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(send_message_url, json=payload, headers=headers)
        print(f"Auto-reply status: {response.status_code}, response: {response.text}")
    except Exception as e:
        print(f"Failed to send auto-reply: {e}")

def get_latest_assistant_message(messages, user_message_time):
    """
    Retrieve the latest assistant message after a given timestamp.
    """
    for msg in reversed(messages.data):
        if msg.role == "assistant" and msg.created_at > user_message_time:
            return msg.content[0].text.value
    return "Sorry, I couldn't process your request."

# Function to handle OpenAI replies
def get_openai_reply(user_id, message_text):
    global user_threads

    try:
        print(f"User ({user_id}) says: {message_text}")

        # Check if the user already has a thread
        if user_id not in user_threads:
            # Create a new thread and run
            run = client.beta.threads.create_and_run(
                assistant_id=ASSISTANT_ID,
                thread={"messages": [{"role": "user", "content": message_text}]}
            )
            user_threads[user_id] = {
                "thread_id": run.thread_id,
                "run_id": run.id,
            }
            print(f"Started a new thread for user {user_id} with ID: {run.thread_id}")
        else:
            # Reuse existing thread and handle active run
            thread_id = user_threads[user_id]["thread_id"]

            # Add user's new message
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_text,
            )

            # Start a new run for the thread
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=ASSISTANT_ID
            )
            print("AssID",run.assistant_id)
            user_threads[user_id]["run_id"] = run.id

        # Wait for the assistant's response
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=user_threads[user_id]["thread_id"],
                run_id=user_threads[user_id]["run_id"]
            )
            if run_status.status == "completed":
                break
            print(f"Waiting for assistant's response for user {user_id}...")
            sleep(2)

        # Retrieve the final response
        thread_id = user_threads[user_id]["thread_id"]
        messages = client.beta.threads.messages.list(thread_id)

        # Get the latest assistant reply after the user's message
        user_message_time = max(
            msg.created_at
            for msg in messages.data
            if msg.role == "user" and msg.content[0].text.value == message_text
        )
        assistant_reply = get_latest_assistant_message(messages, user_message_time)

        print(f"Assistant ({user_id}) Reply: {assistant_reply}")
        return assistant_reply

    except Exception as e:
        print(f"Error connecting to OpenAI Assistant for user {user_id}: {e}")
        return "Sorry, something went wrong."

# Webhook handler for WhatsApp messages
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    if data and "messages" in data:
        for message in data["messages"]:
            if message.get("from_me", False):
                continue

            chat_id = message.get("chat_id")
            user_message = message.get("text", {}).get("body", "")
            print(f"User message from {chat_id}: {user_message}")

            # Get assistant reply
            assistant_reply = get_openai_reply(chat_id, user_message)
            print(f"Assistant Reply for {chat_id}: {assistant_reply}")

            # Send reply back to WhatsApp
            send_auto_reply(chat_id, assistant_reply)

    return jsonify({"status": "success"}), 200

# Flask app entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)