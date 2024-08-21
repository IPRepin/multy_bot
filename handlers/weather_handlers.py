import datetime

import logging

import requests

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from data.weather_city_table import get_city_by_user_id, update_city
from keyboards.replay_keyboards import get_main_keyboard
from keyboards.weathr_keyboards.inline_keyboards import choose_another_city_keyboard
from utils.states import City

weather_router = Router()
logger = logging.getLogger(__name__)


@weather_router.message(F.text == "🌤Узнать погоду")
async def weather(message: types.Message,
                  state: FSMContext,
                  session: AsyncSession):
    city = await get_city_by_user_id(session,
                                     message.from_user.id)
    if city.cities != 'no_city':
        await get_weather(session=session, message=message, )
    else:
        await state.set_state(City.NAME)
        await message.answer("Напишите мне название города (например: Москва)"
                             " и я пришлю сводку погоды.")


@weather_router.callback_query(F.data == "another_city")
async def another_city(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(City.NAME)
    main_menu = await get_main_keyboard()
    await call.message.answer("Напишите новое название города (например: Москва) "
                              "и нажмите '🌤Узнать погоду'.",
                              reply_markup=main_menu)
    await call.answer()


@weather_router.message(City.NAME)
async def add_name_city(message: types.Message,
                        state: FSMContext,
                        session: AsyncSession):
    await state.update_data(cities=message.text)
    data = await state.get_data()
    await state.clear()
    await update_city(session=session,
                      message=message,
                      data=data.get("cities"))
    await message.answer("Нажмите '🌤Узнать погоду'", reply_markup=await get_main_keyboard())


async def get_weather(message: types.Message,
                      session: AsyncSession):
    city = await get_city_by_user_id(session, message.from_user.id)
    code_to_smele = {
        'Clear': "Ясно \U00002600",
        'Clouds': "Облачно \U00002601",
        'Rain': "Дождь \U00002614",
        'Drizzle': "Дождь \U00002614",
        'Thunderstorm': "Гроза \U000026A1",
        'Snow': "Снег \U0001F328",
        'Mist': "Туман \U0001F32B"
    }
    try:
        request_open_weather = requests.get(
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city.cities},&"
                f"lang=ru&appid={settings.OPEN_WEATHER_TOKEN}&units=metric"
        )
        data_weather = request_open_weather.json()
        name = data_weather['name']
        cur_weather = data_weather['main']['temp']
        humidity = data_weather['main']['humidity']
        pressure = data_weather['main']['pressure']

        weather_forecast = data_weather['weather'][0]['main']
        if weather_forecast in code_to_smele:
            wd = code_to_smele[weather_forecast]
        else:
            wd = 'Посмотри в окно, там непонятно что...'

        sunrise = datetime.datetime.fromtimestamp(data_weather['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data_weather['sys']['sunset'])
        length_of_the_day = (datetime.datetime.fromtimestamp(data_weather['sys']['sunset']) -
                             datetime.datetime.fromtimestamp(
                                 data_weather['sys']['sunrise']))
        menu = await choose_another_city_keyboard()
        await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                             f'🔸Погода в городе: {name}\n'
                             f'🔸Температура: {cur_weather}С°\n'
                             f'🔸{wd}\n'
                             f'🔸Давление: {pressure} мм.рт.ст.\n'
                             f'🔸Влажность: {humidity}\n'
                             f'🔸Восход: {sunrise}\nЗакат: {sunset}\n'
                             f'🔸Длинна светового дня: {length_of_the_day}\nХорошего дня!',
                             reply_markup=menu
                             )
    except KeyError as error:
        logger.error(error)
        await message.answer("❗Название города введено неправильно, введите город повторно❗",
                             reply_markup=await choose_another_city_keyboard())
