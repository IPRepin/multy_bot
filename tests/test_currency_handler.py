from handlers.currency_handlers import send_currency, currency_choose_callback, currency_callback

from pycbrf import ExchangeRates

import pytest
from unittest import mock
from aiogram import types

from unittest.mock import AsyncMock, patch

from datetime import datetime


class TestCurrencyHandler:
    @pytest.mark.asyncio
    async def test_send_currency(self):
        # Создаем mock-объект для message
        message = mock.MagicMock(spec=types.Message)
        message.from_user = mock.MagicMock()
        message.from_user.first_name = "TestUser"
        message.answer = AsyncMock()

        # Создаем mock-объект для rates
        rates = ExchangeRates(str(datetime.now())[:10])
        choose_another_currency_keyboard = AsyncMock()

        # Патчим оригинальные функции в вашем модуле

        with mock.patch('handlers.currency_handlers.choose_another_currency_keyboard',
                        choose_another_currency_keyboard):
            # Вызываем тестируемую функцию
            await send_currency(message)

            # Проверяем, что функции были вызваны
            choose_another_currency_keyboard.assert_called_once()

            # Проверяем, что сообщение отправлено корректно
            expected_text = (
                f"Обменный курс валют от ЦБ РФ на {str(datetime.now())[:10]}:\n"
                f"🇺🇸 1{rates['USD'].code} - {rates['USD'].rate}₽\n"
                f"🇪🇺 1{rates['EUR'].code} - {rates['EUR'].rate}₽\n"
                f"🇨🇳 1{rates['CNY'].code} - {rates['CNY'].rate}₽\n"
                f"🇨🇭 1{rates['CHF'].code} - {rates['CHF'].rate}₽\n"
            )
            message.answer.assert_called_once_with(
                expected_text,
                reply_markup=await choose_another_currency_keyboard()
            )

    @pytest.mark.asyncio
    async def test_currency_choose_callback(self):
        callback_query = mock.MagicMock(spec=types.CallbackQuery)
        callback_query.data = "another_currency"

        message = mock.MagicMock(spec=types.Message)
        message.answer = AsyncMock()
        callback_query.message = message

        choose_country_keyboard = AsyncMock()
        callback_query.answer = AsyncMock()

        with mock.patch('handlers.currency_handlers.choose_another_currency_keyboard', choose_country_keyboard):
            await currency_choose_callback(callback_query)
            message.answer.assert_called_once_with("Выберите валюту", reply_markup=mock.ANY)
        callback_query.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_currency_callback(self):
        # Создаем асинхронный mock объект для callback_query
        callback_query = AsyncMock(spec=types.CallbackQuery)
        callback_query.data = "currency_USD"

        # Устанавливаем асинхронный mock для метода answer
        async_answer = AsyncMock()
        callback_query.answer = async_answer

        message = mock.MagicMock(spec=types.Message)
        message.answer = AsyncMock()
        callback_query.message = message

        # Создаем mock для ExchangeRates
        rates = mock.MagicMock()
        rates.__getitem__.return_value = mock.Mock(code='USD', rate=75.0)

        with patch('handlers.currency_handlers.ExchangeRates', return_value=rates):
            await currency_callback(callback_query)

        currency_cod = callback_query.data.split("_")[-1]
        expected_text = f"1{rates[currency_cod].code} - {rates[currency_cod].rate}₽\n"
        message.answer.assert_called_once_with(expected_text)
