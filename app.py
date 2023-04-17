from flask import Flask, request
import requests
from message_handler import handle_message
import logging
import wikipedia


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
# Replace <your-bot-token> with your actual bot token
BOT_TOKEN = "6195203641:AAECYUhCZnzMuTkVCSsfBbE1m2IdZ2rPzLg"
WEBHOOK_URL = "https://9058-82-117-219-86.eu.ngrok.io"


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
    message = update["message"]
    logging.debug(update)

    message_text = update["message"]["text"]
    # text = message.get("text")

    chat_id = message["chat"]["id"]

    if message_text.startswith("/wiki"):
        print("wiki request acquired...")
        search_term = message_text.split()[1].strip()
        result = search_wikipedia(search_term)
        sentences = result.split('.')
        first_three_sentences = '.'.join(sentences[:3]) + '.'
        send_message(chat_id, first_three_sentences)
        return result
    elif "message" in update:
        message = update["message"]
        handle_message(message)

    return 'OK'


@app.route("/")
def index():
    return "Hello, world!"


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()


def search_wikipedia(search_term):
    results = wikipedia.search(search_term)
    if not results:
        return "Sorry, no results found for '{}'".format(search_term)
    else:
        page = wikipedia.page(results[0])
        return page.content


if __name__ == "__main__":
    app.run(debug=True)
