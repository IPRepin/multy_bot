from unittest.mock import AsyncMock

import pytest
from unittest import mock
from aiogram import types

from handlers.commands_handler import start_command, help_command


class TestCommandsHandler:
    @pytest.mark.asyncio
    async def test_start_command(self):
        # Создаем mock-объект для message
        message = mock.MagicMock(spec=types.Message)
        message.from_user = mock.MagicMock()
        message.from_user.first_name = "TestUser"
        message.answer = AsyncMock()

        # Создаем mock-объект для session
        session = mock.MagicMock()

        # Создаем mock-функции
        add_user = AsyncMock()
        add_city = AsyncMock()
        get_main_keyboard = AsyncMock(return_value="mocked_keyboard")

        # Патчим оригинальные функции в вашем модуле
        with mock.patch("handlers.commands_handler.add_user", add_user):
            with mock.patch('handlers.commands_handler.add_city', add_city):
                with mock.patch('handlers.commands_handler.get_main_keyboard', get_main_keyboard):
                    # Вызываем тестируемую функцию
                    await start_command(message, session)

                    # Проверяем, что функции были вызваны
                    add_user.assert_called_once_with(session, message)
                    add_city.assert_called_once_with(session, message)
                    get_main_keyboard.assert_called_once()

                    # Проверяем, что метод answer был вызван с ожидаемыми аргументами
                    message.answer.assert_called_once_with(
                        "Привет TestUser!\n"
                        "🤖Я ваш полезный помощник в Telegram.\n"
                        "Я могу показать прогноз погоды 🌦️,\nактуальные курсы валют 💱\n"
                        "и помочь с управлением вашими задачами 📝.\n"
                        "Выбери нужный пункт меню, чтобы начать!🚀",
                        reply_markup="mocked_keyboard"
                    )

    @pytest.mark.asyncio
    async def test_cmd_help(self):
        message = AsyncMock()
        await help_command(message)
        message.reply(
            "Вот что я умею: 🌟\n"
            "\n"
            "/start 🚀: Начать работу с ботом.\n"
            "/help : Помощь.\n"
            "Основное меню:\n"
            "'🌤Узнать погоду' Покажет погоду.\n"
            "'💰Курс валют' Покажет актуальные курсы валют.\n"
            "'📝Задачи' Поможет с управление задачами.\n"
        )
