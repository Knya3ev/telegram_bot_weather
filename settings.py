from handlers import add_city
from default_config import token_bot, api_key

TOKEN_BOT = token_bot # ваш токен телеграм бота
API_KEY = api_key # ваш api ключ, я использовал (https://www.weatherapi.com/)

INTENTS = [
    {
        "name": "Привет",
        "tokens": ("/start",),
        "scenario": None,
        "answer": "Привет {} 👋, этот бот создан для того чтобы узнать актуальную погоду."
                  "Для начала тебе стоит указать город  в котором ты хочешь узнать погоду",
        "buttons": {
            "name": ['Указать город 🏙'],
            "row": 1
        },

    },
    {
        "name": "Указать город",
        "tokens": ("Указать", "город", "Ред.", "город", '/edit_city'),
        "scenario": "add_a_city",
        "answer": None,
        "buttons": None
    },

]
SCENARIO = {
    "add_a_city": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Пожалуйста впишите  город без сокращений ✏",
                "failure_text": "🛑 ОШИБКА: возможно вы используете сокращение или следущие символы '!@#$%^&*()_-'",
                "handler": add_city,
                "next_step": "step2",
            },
            "step2": {
                "text": "✅ Город добавлен!\nТеперь вы можете получать прогноз погоды 🙌 ",
                "handler": None,
                "next_step": None,
            },
        }
    }
}


emoji_dict = {
    'Небольшой снег': 'Небол. снег 🌨',
    'Умеренный снег': 'Умерен. снег 🌨',
    'Дымка': 'Дымка 🌁',
    'Ясно': 'Ясно ☀',
    'Пасмурно': 'Пасмурно ☁',
    'Переменная облачность': 'Пер. облач. 🌤',
    'Переохлажденный туман': 'Хол. туман 🌫',
    'Облачно': 'Облачно ☁',
    'Сильный снег': 'Сильн. снег 🌨',
    'Умеренный или сильный снег': 'У/С снег  🌨',
    'Солнечно': 'Солнечно 🌞',
    'Местами сильный снег': 'Мст. сил. снег ❄'
}

DEFAULT_ANSWER = '🤷‍♂️ Не знаю как на это ответить\n' \
                 'Вы можете:\n' \
                 'узнать прогноз /weather\n' \
                 'изменить город /edit_city\n' \
                 'вернуться в самое начало /start'