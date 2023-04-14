from flask import Flask, request
import requests

app = Flask(__name__)

# Replace <your-bot-token> with your actual bot token
BOT_TOKEN = "6195203641:AAECYUhCZnzMuTkVCSsfBbE1m2IdZ2rPzLg"
WEBHOOK_URL = "http://localhost:5000/"

# Set up webhook for the Telegram bot
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
response = requests.post(url)

if response.ok:
    print("Webhook set up successfully!")
else:
    print("Error setting up webhook:", response.text)


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def process_update():
    update = request.get_json()
    # Process the update here
    return "OK"


@app.route("/")
def index():
    return "Hello, world!"


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def handle_bot_update():
    update = request.get_json()
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text")

    if text == "hi":
        send_message(chat_id, "Hi!")

    # Do something with the message text
    send_message(chat_id, f"You said: {text}")

    return "OK"


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


if __name__ == "__main__":
    app.run(debug=True)
