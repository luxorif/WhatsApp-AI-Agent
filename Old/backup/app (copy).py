from flask import Flask, request, jsonify
from whatsapp import handle_whatsapp_message
import config

# Initialize Flask app
app = Flask(__name__)

# Webhook for handling incoming WhatsApp messages
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    return handle_whatsapp_message(request.json)

# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.FLASK_PORT)