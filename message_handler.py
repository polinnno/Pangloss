import app


def handle_message(message):
    text = message.get("text")
    chat_id = message["chat"]["id"]

    if text == "hi":
        app.send_message(chat_id, "Hiiiiii!")
    elif text == "bye":
        app.send_message(chat_id, "Goodbye!")
    elif text == "what":
        app.send_message(chat_id, "nothing")
    else:
        app.send_message(chat_id, "I didn't understand that.")
