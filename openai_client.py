from openai import OpenAI
from time import sleep
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Track threads for users
user_threads = {}

class OpenAIClient:
    def __init__(self, api_key, assistant_id):
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id
        self.user_threads = {}

    def get_or_create_thread(self, user_id, message_text):
        """
        Creates a new thread for a user if one doesn't exist,
        or retrieves the existing thread for further communication.
        """
        if user_id not in self.user_threads:
            # Create a new thread and run
            run = self.client.beta.threads.create_and_run(
                assistant_id=self.assistant_id,
                thread={"messages": [{"role": "user", "content": message_text}]}
            )
            self.user_threads[user_id] = {
                "thread_id": run.thread_id,
                "run_id": run.id,
            }
            logging.info(f"Created new thread for {user_id} with thread ID: {run.thread_id}")
        else:
            # Reuse existing thread
            thread_id = self.user_threads[user_id]["thread_id"]
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_text,
            )
            # Start a new run for this thread
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )
            self.user_threads[user_id]["run_id"] = run.id
            logging.info(f"Reused thread {thread_id} for {user_id}, new run ID: {run.id}")

    def wait_for_response(self, thread_id, run_id):
        """
        Polls the API until the assistant's response is ready.
        """
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if run_status.status == "completed":
                break
            logging.info(f"Waiting for assistant's response on thread {thread_id}...")
            sleep(2)


    def get_latest_assistant_message(self, messages, user_message_time):
        """
        Fetches the latest assistant message from a thread after the user's message time.
        """
        latest_message = next(
            (msg.content[0].text.value for msg in reversed(messages.data)
             if msg.role == "assistant" and msg.created_at > user_message_time),
            "Sorry, I couldn't process your request."
        )
        return latest_message

    def get_reply(self, user_id, message_text):
        """
        Main method to handle getting a reply from OpenAI assistant.
        """
        try:
            # Ensure the thread exists and is updated with the user message
            self.get_or_create_thread(user_id, message_text)

            # Get thread and run IDs
            thread_id = self.user_threads[user_id]["thread_id"]
            run_id = self.user_threads[user_id]["run_id"]

            # Wait for the assistant's response
            self.wait_for_response(thread_id, run_id)

            # Retrieve all messages in the thread
            messages = self.client.beta.threads.messages.list(thread_id)

            # Get the latest assistant reply after the user's message
            user_message_time = max(
                msg.created_at
                for msg in messages.data
                if msg.role == "user" and msg.content[0].text.value == message_text
            )
            assistant_reply = self.get_latest_assistant_message(messages, user_message_time)

            logging.info(f"Assistant reply for {user_id}: {assistant_reply}")
            return assistant_reply

        except Exception as e:
            logging.error(f"Error in OpenAI API for user {user_id}: {e}")
            return "Sorry, something went wrong."
            
# Initialize the OpenAI client
openai_client = OpenAIClient(api_key=API_KEY, assistant_id=ASSISTANT_ID)