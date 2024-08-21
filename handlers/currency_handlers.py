from datetime import datetime

from pycbrf import ExchangeRates

from aiogram import types, Router, F

from keyboards.currency_keyboards.inline_keyboards import choose_another_currency_keyboard, choose_country_keyboard

currency_router = Router()


@currency_router.message(F.text == "💰Курс валют")
async def send_currency(message: types.Message):
    rates = ExchangeRates(str(datetime.now())[:10])
    await message.answer(
        f"Обменный курс валют от ЦБ РФ на {str(datetime.now())[:10]}:\n"
        f"🇺🇸 1{rates['USD'].code} - {rates['USD'].rate}₽\n"
        f"🇪🇺 1{rates['EUR'].code} - {rates['EUR'].rate}₽\n"
        f"🇨🇳 1{rates['CNY'].code} - {rates['CNY'].rate}₽\n"
        f"🇨🇭 1{rates['CHF'].code} - {rates['CHF'].rate}₽\n",
        reply_markup=await choose_another_currency_keyboard()
    )


@currency_router.callback_query(F.data == "another_currency")
async def currency_choose_callback(call: types.CallbackQuery):
    await call.message.answer("Выберите валюту", reply_markup=await choose_country_keyboard())
    await call.answer()


@currency_router.callback_query(F.data.startswith("currency_"))
async def currency_callback(call: types.CallbackQuery):
    currency_cod = call.data.split("_")[-1]
    rates = ExchangeRates(str(datetime.now())[:10])
    await call.message.answer(
        f"1{rates[currency_cod].code} - {rates[currency_cod].rate}₽\n"
    )
    await call.answer()
