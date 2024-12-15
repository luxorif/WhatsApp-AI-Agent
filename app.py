from flask import Flask, request, jsonify
from whatsapp import send_auto_reply, handle_whatsapp_message

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

# Flask app entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)