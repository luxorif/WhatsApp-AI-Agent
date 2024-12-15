from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Global variable to track the thread ID
console_thread_id = None

# Function to get assistant's reply
def get_openai_reply(message_text):
    global console_thread_id

    try:
        print(f"User: {message_text}")

        # Create a new thread if not already initialized
        if not console_thread_id:
            thread = client.beta.threads.create()
            console_thread_id = thread.id
            print(f"Started a new thread with ID: {console_thread_id}")

            # Add system instructions as a special user message
            client.beta.threads.messages.create(
                thread_id=console_thread_id,
                role="user",
                content={message_text}
            )
        else:
            print(f"Using existing thread ID: {console_thread_id}")

        # Add user message to the thread
        client.beta.threads.messages.create(
            thread_id=console_thread_id,
            role="user",
            content=message_text
        )

        # Start the assistant run
        run = client.beta.threads.runs.create(
            thread_id=console_thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for the assistant's response
        while not run.status == "completed":
            print("Waiting for assistant's response...")
            sleep(2)
            run = client.beta.threads.runs.retrieve(
                thread_id=console_thread_id,
                run_id=run.id
            )

        # Retrieve the final response
        messages = client.beta.threads.messages.list(console_thread_id)
        first_message = messages.data[0].content[0].text.value
        assistant_reply = messages.data[-1].content[0].text.value  # Get the latest message
        #print(messages.data)
        print(f"Assistant: {first_message}")
        return first_message


    except Exception as e:
        print(f"Error connecting to OpenAI Assistant: {e}")
        return "Sorry, something went wrong."

# Console-based chat loop
def chat_with_assistant():
    print("Chat with your assistant! Type 'exit' to end the session.\n")
    while True:
        # Get user input
        user_message = input("You: ")
        if user_message.lower() == "exit":
            print("Ending the chat session. Goodbye!")
            break

        # Get assistant's reply
        get_openai_reply(user_message)

# Entry point for console-based chat
if __name__ == '__main__':
    chat_with_assistant()