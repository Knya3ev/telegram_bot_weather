import settings
from telebot import types
from models import User, UserState
import buttans
import logging

log = logging.getLogger('bot')


class BotHandler:
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        self.bt = buttans
        self.settings = settings

    def start_scenario(self, user_id, scenario_name):
        scenario = self.settings.SCENARIO[scenario_name]  # получаем название сценария
        first_step = scenario['first_step']  # получаем первый степ сценария
        step = scenario['steps'][first_step]
        # bot.send_message(user_id, step['text'])  # отправка первого степа из сценария
        UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step, context={})
        return {'text': step['text'], 'buttons': types.ReplyKeyboardRemove(selective=False)}

    def continue_scenario(self, text, state, user_id):  # state данные молдели
        steps = self.settings.SCENARIO[state.scenario_name]['steps']  # из модели по имени сценария получаю степов
        step = steps[state.step_name]  # имя степа из модели
        handler = step['handler']  # если def  будет в другом файлу использовать gettatr
        if handler(city=text.lower(), context=state.context):  # возврощает TRUE в случае если такой город есть
            next_step = steps[step['next_step']]
            if next_step['next_step']:  # если есть следущий степ
                state.step_name = step['next_step']
                return {'text': step['text'], 'buttons': None}
            else:
                user = User.get(user_id=str(user_id))
                if user is not None:
                    log.debug(f'Пользователь c id {user_id} поменял свой город на {state.context["city"]}')
                    user.user_city = state.context['city']
                else:
                    User(user_id=str(user_id), user_city=state.context['city'])
                    log.debug(f'Зарегистрировался Новый пользователь с id {user_id} город {state.context["city"]}')
                state.delete()
            return {'text': next_step['text'], 'buttons': self.bt.in_keyboard(['Погода 🌤'], 1)}
        else:
            log.error(f'Ошибка при добавление города! User_id:{user_id}, text: {text}')
            return {'text': step['failure_text'], 'buttons': None}

    def run(self,):
        state = UserState.get(user_id=str(self.user_id))
        if state is not None:
            return self.continue_scenario(self.text, state, self.user_id)
        else:
            for intent in self.settings.INTENTS:
                if any(token in self.text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        return {'text': intent['answer'], 'buttons': self.bt.in_keyboard(**intent['buttons'])}
                    else:
                        return self.start_scenario(self.user_id, intent['scenario'])

            return {'text': self.settings.DEFAULT_ANSWER, 'buttons': types.ReplyKeyboardRemove(selective=False)}


def translate_city(city):
    """Переводит строку  RU > ENG"""
    d = {
        'а': 'a', 'к': 'k', 'х': 'h', 'б': 'b', 'л': 'l', 'ц': 'c', 'в': 'v', 'м': 'm', 'ч': 'ch',
        'г': 'g', 'н': 'n', 'ш': 'sh', 'д': 'd', 'о': 'o', 'щ': 'shh', 'е': 'e', 'п': 'p', 'ъ': '*',
        'ё': 'jo', 'р': 'r', 'ы': 'y', 'ж': 'zh', 'с': 's', 'ь': "'", 'з': 'z', 'т': 't', 'э': 'je',
        'и': 'i', 'у': 'u', 'ю': 'ju', 'й': 'j', 'ф': 'f', 'я': 'ya', ' ': ' '
    }
    translate = ''
    for char in city.lower():
        translate += d[char] if char in d else ''
    return translate


def add_city(city, context):

    """ Проверяет существование города """

    with open('cities.txt', 'r', encoding='utf-8') as file_cities:
        set_city = {i.lower().replace('-', ' ') for i in file_cities.read().split(', ') if i != ''}
        if city.lower() in set_city:
            context['city'] = translate_city(city)
        return 1 if city in set_city else 0
