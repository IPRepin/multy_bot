from aiogram import types, Router

from keyboards.replay_keyboards import get_main_keyboard

empty_handler_router = Router()


@empty_handler_router.message()
async def get_empty_handler(message: types.Message):
    await message.reply("Выбери действие из главного меню", reply_markup=await get_main_keyboard())
