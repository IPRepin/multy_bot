from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def choose_another_currency_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="💱Выбрать другую валюту", callback_data="another_currency")
    return keyboard.as_markup()


async def choose_country_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🇹🇷TRY", callback_data="currency_TRY"),
        InlineKeyboardButton(text="🇮🇳₹", callback_data="currency_INR"),
        InlineKeyboardButton(text="🇰🇷KRW", callback_data="currency_KRW"),
        InlineKeyboardButton(text="🇧🇾BYN", callback_data="currency_BYN"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🇺🇿UZS", callback_data="currency_UZS"),
        InlineKeyboardButton(text="🇯🇵JPY", callback_data="currency_JPY"),
        InlineKeyboardButton(text="🇬🇧GBP", callback_data="currency_GBP"),
        InlineKeyboardButton(text="🇪🇬EGP", callback_data="currency_EGP"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🇰🇿KZT", callback_data="currency_KZT"),
        InlineKeyboardButton(text="🇹🇭THB", callback_data="currency_THB"),
        InlineKeyboardButton(text="🇬🇪GEL", callback_data="currency_GEL"),
        InlineKeyboardButton(text="🇦🇿AZN", callback_data="currency_AZN"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🇦🇪AED", callback_data="currency_AED"),
        InlineKeyboardButton(text="🇶🇦QAR", callback_data="currency_QAR"),
        InlineKeyboardButton(text="🇻🇳VND", callback_data="currency_VND"),
        InlineKeyboardButton(text="🇸🇬SGD", callback_data="currency_SGD"),
    )
    return keyboard.as_markup()
