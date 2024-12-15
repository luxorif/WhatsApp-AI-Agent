from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
import os

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID="asst_fllCyHROOJfQNiSIMuR5gzRZ"

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)
assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
print(assistant)

def get_answer(run,thread):
    while not run.status == "completed":
        print(f'waiting for answer')
        sleep(1)

        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread.id)

    try:
        answer = messages.data[0].content[0].text.value

    except Exception as e:
        print(e)
        answer = ''
    return answer
    

def ask_assistant(message_text):
    print(f'asking the assistant: {message_text}')

    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_text
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    answer = get_answer(run,thread)
    print(f'assistant response: {answer}')
    return answer

if __name__=='__main__':
    ask_assistant("hello")