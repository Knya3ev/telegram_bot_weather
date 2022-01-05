import telebot
"""dasdasdasdad
"""
markup_menu = telebot.types.InlineKeyboardMarkup(row_width=3)
markup_menu.add(*[
    telebot.types.InlineKeyboardButton(text='сегодня', callback_data='0'),
    telebot.types.InlineKeyboardButton(text='завтра', callback_data='1'),
    telebot.types.InlineKeyboardButton(text='на 3 дня', callback_data='2'),
    telebot.types.InlineKeyboardButton(text='🏢 изменить город', callback_data='город'),
])


def in_chat(data, number):
    button = telebot.types.InlineKeyboardMarkup(row_width=1)
    button.add(telebot.types.InlineKeyboardButton(text='Подробнее', callback_data=f'hour {data} {number}'))
    return button


def in_keyboard(name, row):
    if name:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=row)
        markup.add(*[telebot.types.KeyboardButton(i) for i in name])
        return markup
    else:
        return telebot.types.ReplyKeyboardRemove(selective=False)
