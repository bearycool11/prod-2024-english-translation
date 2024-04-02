import datetime

import requests
import telebot

from database import get_session
from database.models import DBTask
from utils import task


@task
def send_message(bot_token, channel_id, message_text, post_id):
    bot = telebot.TeleBot(bot_token)
    try:
        message = bot.send_message(chat_id=channel_id, text=message_text)
        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                      json={"post_id": post_id, "post_status": "SENT_OK", "telegram_message_id": message.message_id})
        with get_session() as session:
            task_collect_metrics = DBTask(handler="collect_metrics", planned_time=datetime.datetime.now(),
                                          next_run_delta=60 * 60, arguments={"post_id": post_id,
                                                                             "telegram_message_id": message.message_id,
                                                                             "channel_id": channel_id})
            session.add(task_collect_metrics)
            session.commit()
    except:
        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                      json={"post_id": post_id, "post_status": "SENT_ERROR", "telegram_message_id": None})


@task
def collect_metrics(post_id, telegram_message_id, channel_id):
    pass
