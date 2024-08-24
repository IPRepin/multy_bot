from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌤Узнать погоду")],
            [KeyboardButton(text="💰Курс валют")],
            [KeyboardButton(text="🤖AI маркетолог")],
        ],
        resize_keyboard=True)
    return main_keyboard
