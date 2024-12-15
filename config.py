import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
API_TOKEN = os.getenv("API_TOKEN")
SEND_MESSAGE_URL = os.getenv("SEND_MESSAGE_URL")