import datetime

import requests
import telebot

from database import get_session
from database.models import DBTask
from utils import task


@task
def send_message(bot_token, channel_id, telegram_channel_id, message_text, post_id):
    try:
        bot = telebot.TeleBot(bot_token)
        message = bot.send_message(chat_id=telegram_channel_id, text=message_text)
        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                      json={"post_id": post_id, "post_status": "SENT_OK", "telegram_message_id": message.message_id,
                            "channel_id": channel_id, "chat_username": message.chat.username,
                            "clear_planned_time": False})
    except:
        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                      json={"post_id": post_id, "post_status": "SENT_ERROR", "telegram_message_id": None,
                            "channel_id": None, "chat_username": None, "clear_planned_time": False})
