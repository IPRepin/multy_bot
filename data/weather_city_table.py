import logging

from aiogram import types

from data.models import WeatherCity

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def add_city(
        session: AsyncSession,
        message: types.Message,
):
    """Создание нового города"""
    try:
        session.add(WeatherCity(
            user_id=message.from_user.id,
        ))
        await session.commit()
        logger.info(f"Город для пользователя {message.from_user.id} добавлен")
    except IntegrityError as error:
        logger.error(f"Город для пользователя {message.from_user.id} уже существует")
        logger.error(error)
        await session.rollback()


async def all_citys(session: AsyncSession):
    """Получение городов"""
    query = select(WeatherCity)
    result = await session.execute(query)
    return result.scalars().all()


async def get_city_by_user_id(session: AsyncSession, user_id: int):
    """Получение города по user_id"""
    query = select(WeatherCity).where(user_id == WeatherCity.user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_city(session: AsyncSession, message: types.Message,
                      data: dict):
    """Обновление города"""
    query = update(WeatherCity).where(WeatherCity.user_id == message.from_user.id).values(
        cities=data,
    )
    await session.execute(query)
    await session.commit()


async def delete_city(session: AsyncSession, message: types.Message):
    """Удаление города"""
    query = delete(WeatherCity).where(WeatherCity.user_id == message.from_user.id)
    await session.execute(query)
    await session.commit()
