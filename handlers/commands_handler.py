from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from data.user_table import add_user
from data.weather_city_table import add_city
from keyboards.replay_keyboards import get_main_keyboard

command_router = Router()


@command_router.message(CommandStart())
async def start_command(message: types.Message, session: AsyncSession):
    await add_user(session, message)
    await add_city(session, message)
    main_menu = await get_main_keyboard()
    await message.answer(
        f"Привет {message.from_user.first_name}!\n"
        "🤖Я AI помощник маркетолога.\n"
        "Я знаю множество инструментов от Яндекс директ, до CRM систем и способен помочь с настройкой. "
        "Я могу написать как продающие тексты для объявлений, так и оптимизированные SEO статьи. "
        "Отвечу на любые вопросы по интернет маркетингу и подкреплю ответ ссылками на нужные ресурсы.\n"
        "Помогу с анализом статистики, проверю текущее состояние рынка и многое другое!\n"
        "⛔К сожалению я пока не умею вести диалоги и отвечаю в формате 'Вопрос-ответ', "
        "но скоро научусь, а еще мой"
        " кожаный создатель обещал в скором будущем научить меня генерации изображений.\n"
        "Я также могу показать прогноз погоды 🌦️\n"
        "и актуальные курсы валют 💱\n"
        "Выбери нужный пункт меню, чтобы начать!🚀",
        reply_markup=main_menu,
    )


@command_router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Вот что я умею: 🌟\n"
                         "\n"
                         "/start 🚀: Начать работу с ботом.\n"
                         "/help : Помощь.\n"
                         "Основное меню:\n"
                         "'🌤Узнать погоду' Покажет погоду.\n"
                         "'💰Курс валют' Покажет актуальные курсы валют.\n"
                         "🤖AI помощник маркетолога\n"
                         )


