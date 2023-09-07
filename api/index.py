import os
from fastapi import FastAPI
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

TOKEN = os.environ.get("TOKEN")
app = FastAPI()


@app.get("/")
def index():
    return {"message": "hello world"}


def start(update: Updater, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I am a bot")


def register_handler(dispatcher):
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    register_handler(dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
