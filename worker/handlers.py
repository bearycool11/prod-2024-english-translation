import requests
import telebot

from utils import task


@task
def send_message(bot_token, channel_id, message_text, post_id):
    bot = telebot.TeleBot(bot_token)
    try:
        bot.send_message(chat_id=channel_id, text=message_text)
        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                      json={"post_id": post_id, "post_status": "SENT_OK"})
    except:
        requests.post("http://smm_ya_backend:5437/api/private/set_post_sent_state",
                      json={"post_id": post_id, "post_status": "SENT_ERROR"})
