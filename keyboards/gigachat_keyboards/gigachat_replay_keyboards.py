from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_gigachat_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новый запрос")],
            [KeyboardButton(text="На главное меню")],
        ],
        resize_keyboard=True)
    return main_keyboard
