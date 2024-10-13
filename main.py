import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API = os.getenv('WEATHER_API')

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши название города, чтобы узнать погоду.")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric')
        data = response.json()

        if data.get('cod') != 200:
            bot.send_message(message.chat.id, f"Ошибка: {data.get('message')}")
            return

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        weather_info = (
            f"Погода в городе {city.capitalize()}:\n"
            f"Температура: {temperature}°C\n"
            f"Влажность: {humidity}%\n"
            f"Описание: {weather_description}\n"

        )

        bot.send_message(message.chat.id, weather_info)

    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, "Произошла ошибка при попытке получить данные о погоде.")
        print(e)


bot.polling(non_stop=True)

