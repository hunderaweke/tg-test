import os
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.getenv("TOKEN")

if BOT_TOKEN is None:
    raise ValueError("Telegram bot token not found in environment variable 'TOKEN'")

logging.basicConfig(level=logging.INFO)
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]


@dp.message_handler()
async def echo(msg: types.Message):
    await msg.reply(msg.text)


@app.on_event("startup")
async def startup_event():
    await dp.start_polling()


@app.post("/webhook")
async def webhook(request: Request, webhook_data: TelegramWebhook):
    webhook_url = str(request.base_url) + "/webhook"
    await bot.set_webhook(url=webhook_url)
    update_data = webhook_data.__dict__
    update = types.Update(**update_data)
    await dp.process_update(update)
    return {"message": "ok"}


@app.get("/")
def index():
    return {"Message": "hello"}
