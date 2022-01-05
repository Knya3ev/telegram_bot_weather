import requests
from settings import API_KEY, emoji_dict
import logging
"""
dsadasddsdadsadsad
"""
class Weather:
    def __init__(self, amount_day, name_city, hours=False,):
        self.amount_day = amount_day
        self.name_city = name_city
        self.hours = hours
        self.api_key = API_KEY

    def convert_m(self, n):
        return round(n * 0.277, 1)

    def convert_data(self, data):
        months_ru = {1: 'Января',
                     2: 'Февраля',
                     3: 'Марта',
                     4: 'Апреля',
                     5: 'Мая',
                     6: 'Июня',
                     7: 'Июля',
                     8: 'Августа',
                     9: 'Сентября',
                     10: 'Октября',
                     11: 'Ноября',
                     12: 'Декабря'}
        y, m, d = map(int, data.split('-'))
        return f'{d} {months_ru[m]}'

    def convert_weather_text(self, text: str):
        try:
            emoji = emoji_dict[text.strip()]
            return emoji
        except KeyError as exc:
            log.error(f'KeyError: {exc}')
            return text

    def get_weather(self, days, api_key, name_city):
        x = requests.get(
            f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={name_city}&days={days + 1}&lang=RU')
        return x.json()

    def run(self):
        api_response = self.get_weather(self.amount_day, self.api_key, self.name_city)
        return self.check_date_days(api_response, self.hours)

    def check_date_days(self, api_response, hours=False):
        name_city = api_response['location']['name']
        weather_dh = []

        for days in api_response['forecast']['forecastday']:
            if hours:
                if days['date'] == hours:
                    h = set(filter(lambda x: int(x.split(':')[0]) % 2 == 1,
                                   [i['time'].split(' ')[1] for i in days['hour']]))

                    for hour in days['hour']:
                        if hour['time'].split()[1] in h:
                            weather_dh.append([hour['time'].split()[1], hour['temp_c'],
                                               hour['precip_mm'], hour['condition']['text']])

                    weather_dh.append(['время', 'темпер.', 'осадки', 'описание'])
                    weather_dh.append(self.convert_data(days['date']))
                    return self.string_weather(weather_dh, hours)
            else:
                day = days['day']
                res = [self.convert_data(days['date']),
                       self.convert_weather_text(day['condition']['text']), day['avgtemp_c'],
                       day['mintemp_c'], day['maxtemp_c'], self.convert_m(n=day['maxwind_kph']), day['totalprecip_mm'],
                       days['date']]
                weather_dh.append(self.string_weather(res))

        weather_dh.append(name_city)
        return weather_dh

    def string_weather(self, list_weather, hours=False):
        if hours:
            data, l1 = [list_weather.pop() for _ in range(2)]
            string = f'{data}  🗓' \
                     f'\n{l1[0].rjust(1)} {l1[1].rjust(5)} {l1[2].rjust(5)}  {l1[3].rjust(5)}\n'
            for line in list_weather:
                t, tp, os, text = list(map(str, line))
                n = 4 if len(tp) == 5 else 5
                string += f'|{t.rjust(1)}| {tp.rjust(5)} {os.rjust(n)}мм.' \
                          f' {self.convert_weather_text(text.rjust(5))}' + '\n'
            return string
        else:
            date = list_weather.pop()
            string = "{} {}\nсредняя  температура  {}🌡" \
                     "\nмин. и макс. от {} до {}" \
                     "\nветер = {} м./c. 💨" \
                     "\nколичество осадков= {} мм 📏".format(*list_weather)
            return {date: string}
