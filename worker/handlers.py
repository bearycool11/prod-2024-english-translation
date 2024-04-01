import telebot

from utils import task


@task
def send_message(bot_token, channel_id, message_text, post_id):
    bot = telebot.TeleBot(bot_token)
    try:
        bot.send_message(chat_id=channel_id, text=message_text, parse_mode="MarkdownV2")
        # ok
    except:
        # error
        pass
