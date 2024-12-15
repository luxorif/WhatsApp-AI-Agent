from app import app  # Flask app
import openai_client  # Initialize OpenAI client
import whatsapp  # WhatsApp handling logic
import logging
from logging.handlers import RotatingFileHandler

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=5),  # Log to file (5 MB per file, 5 backups)
    ],
)

# Test logging
logging.info("Logging initialized. This will appear in both the console and the log file.")

if __name__ == "__main__":
    logging.info("Starting the application...")
    app.run(host="0.0.0.0", port=5000)