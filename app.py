from flask import Flask, request
import requests
from message_handler import handle_message
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
# Replace <your-bot-token> with your actual bot token
BOT_TOKEN = "6195203641:AAECYUhCZnzMuTkVCSsfBbE1m2IdZ2rPzLg"
WEBHOOK_URL = "https://ba61-89-216-22-220.eu.ngrok.io"


response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo")
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error checking webhook status: {response.status_code} {response.reason}")


# Set up webhook for the Telegram bot
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
response = requests.post(url)

if response.ok:
    print("Webhook set up successfully!")
else:
    print("Error setting up webhook:", response.text)


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def handle_bot_update():

    update = request.get_json()
    logging.info(f"Received update: {update}")
    print(update)
    print("ok")
    message = update["message"]
    handle_message(message)

    return "OK"


@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()

    print("before")
    message = update["message"]
    logging.debug(update)
    handle_message(message)
    print("after")
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text")
        if text == "hi":
            send_message(chat_id, "Hi <3 !")

    return 'OK'


@app.route("/")
def index():
    return "Hello, world!"


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


if __name__ == "__main__":
    app.run(debug=True)
