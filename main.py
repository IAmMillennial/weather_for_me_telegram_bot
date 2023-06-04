import os
import datetime
import requests
import math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 


bot = Bot(token='6053513952:AAEyJrWSPJojUgi3rTtm5I8Q6PTxu4mtI-I')
dp = Dispatcher(bot)


code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
   	await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")


@dp.message_handler()
async def get_weather(message: types.Message):
    
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text.lower()}&lang=ru&units=metric&appid=3a40e69db58d95f403f39ddc58402b92")
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        
        # получаем время рассвета и преобразуем его в читабельный формат
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        
        # то же самое проделаем со временем заката
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        
        # продолжительность дня
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # получаем значение погоды
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            # если эмодзи для погоды нет, выводим другое сообщение
            wd = "Посмотри в окно, я не понимаю, что там за погода..."
        
        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"Хорошего дня!"
                            )
    except:
        await message.reply("Проверьте название города!")
    
    
if __name__ == "__main__":
	executor.start_polling(dp)