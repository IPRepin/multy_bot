import pytest
from unittest import mock
from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.weather_handlers import weather, another_city
from utils.states import City


class TestWeatherHandlers:
    @pytest.mark.asyncio
    async def test_weather_handler(self):
        # Создаем mock объекты для message, state и session
        message = mock.MagicMock(spec=types.Message)
        state = mock.MagicMock()
        session = mock.AsyncMock(spec=AsyncSession)

        # Создаем mock объект для from_user
        from_user = mock.MagicMock()
        from_user.id = 123  # Устанавливаем ID пользователя

        # Устанавливаем from_user для message
        message.from_user = from_user

        # Устанавливаем данные для message
        message.text = "🌤Узнать погоду"

        # Mock функции get_city_by_user_id
        mock_city = mock.MagicMock(spec=City)
        mock_city.cities = 'Moscow'  # Предположим, что город у пользователя есть
        get_city_mock = mock.AsyncMock(return_value=mock_city)

        # Mock функции get_weather
        get_weather_mock = mock.AsyncMock()

        # Заменяем оригинальные функции на mock-версии в контексте теста
        with mock.patch('handlers.weather_handlers.get_city_by_user_id', get_city_mock):
            with mock.patch('handlers.weather_handlers.get_weather', get_weather_mock):
                # Вызываем обработчик сообщения
                await weather(message=message, state=state, session=session)

        # Проверяем вызовы функций
        get_city_mock.assert_awaited_once_with(session, from_user.id)
        if mock_city.cities != 'no_city':
            get_weather_mock.assert_awaited_once_with(session=session, message=message)
        else:
            state.set_state.assert_awaited_once_with(City.NAME)
            message.answer.assert_called_once_with(
                "Напишите мне название города (например: Москва) и я пришлю сводку погоды."
            )

    @pytest.mark.asyncio
    async def test_another_city_handler(self):
        callback_query = mock.AsyncMock(spec=types.CallbackQuery)
        state = mock.AsyncMock(spec=FSMContext)

        message = mock.AsyncMock(spec=types.Message)
        message.answer = mock.AsyncMock()  # Устанавливаем mock для метода answer
        callback_query.message = message

        # Мокаем метод answer у callback_query
        callback_query.answer = mock.AsyncMock()

        await another_city(callback_query, state)

        # Проверяем вызовы функций
        state.set_state.assert_called_once_with(City.NAME)
        callback_query.message.answer.assert_called_once_with(
            "Напишите новое название города (например: Москва) и нажмите '🌤Узнать погоду'.",
            reply_markup=mock.ANY
        )
        callback_query.answer.assert_awaited_once()
