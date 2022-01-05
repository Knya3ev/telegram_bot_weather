"""python version = 3.8.7"""
import telebot
from settings import TOKEN_BOT
from handlers import BotHandler
from models import User
from pony.orm import db_session
import buttans as bt
from get_weather import Weather
import logging

bot = telebot.TeleBot(TOKEN_BOT)
log = logging.getLogger('bot')
log.setLevel(logging.DEBUG)


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.txt', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", '%Y-%d_%B-%H:%M'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

@bot.message_handler(content_types=['text'])
@db_session
def get_text_messages(message):
    user_id = message.from_user.id
    bot_handler = BotHandler(user_id=user_id, text=message.text)
    if message.text:
        if message.text.lower() in ('погода', 'погода 🌤', '/weather'):
            bot.send_message(user_id, text='🌤 Погода', reply_markup=bt.markup_menu)
        else:
            send = bot_handler.run()  # возврощает text и buttons в виде словаря
            bot.send_message(message.from_user.id, send['text'].format(message.from_user.first_name),
                             reply_markup=send['buttons'])


@bot.callback_query_handler(func=lambda call: True)
@db_session
def callback_query(callback_query: telebot.types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = User.get(user_id=str(user_id))
    bot_handler = BotHandler(user_id=user_id, text=callback_query.data)
    log.debug(f'USER-({user_id}) запрос-({callback_query.data})')
    if callback_query.data == 'город':
        send = bot_handler.run()
        bot.send_message(callback_query.from_user.id, send['text'], reply_markup=send['buttons'])
        return

    if callback_query.data.isdigit():
        i = 0
        response = Weather(amount_day=int(callback_query.data), name_city=user.user_city, ).run()
        bot.send_message(callback_query.from_user.id, text=f'🏙 {response.pop()}')
        for day in response:
            for key, values in day.items():
                bot.send_message(user_id, text=values, reply_markup=bt.in_chat(key, i))
                i += 1
        return

    if 'hour' in callback_query.data:
        x, data, number = callback_query.data.split(' ')
        response = Weather(amount_day=int(number), name_city=user.user_city, hours=data).run()
        bot.send_message(user_id, response)
        return

    else:
        bot.send_message(user_id, text='кнопка в разработке')


if __name__ == '__main__':
    configure_logging()
    bot.polling(none_stop=True, interval=0)
