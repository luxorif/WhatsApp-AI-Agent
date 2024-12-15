from flask import Flask, request, jsonify
from whatsapp import send_auto_reply, handle_whatsapp_message
import os

# Flask app initialization
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the WhatsApp-AI-Agent webhook!"}), 200

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """
    Handles incoming webhook messages from WhatsApp.
    """
    data = request.json
    return handle_whatsapp_message(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)