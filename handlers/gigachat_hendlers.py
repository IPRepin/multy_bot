import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from giga_chat.generators_gigachat import get_gigachat_text
from keyboards.gigachat_keyboards.gigachat_replay_keyboards import get_gigachat_keyboard
from keyboards.replay_keyboards import get_main_keyboard
from utils.states import ChatStates

gigachat_router = Router()
logger = logging.getLogger(__name__)


@gigachat_router.message(F.text.in_(["💬Новый запрос", "🔄На главное меню"]))
async def get_chatting(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(ChatStates.text)
    if message.text == "🔄На главное меню":
        await message.answer("Главное меню", reply_markup=await get_main_keyboard())
    else:
        await message.answer("Введите новый запрос.")


@gigachat_router.message(ChatStates.text)
async def get_chat_response(message: types.Message, state: FSMContext) -> None:
    gpt_answer = await get_gigachat_text(message.text)
    await message.answer(gpt_answer,
                         reply_markup=await get_gigachat_keyboard())


@gigachat_router.message(ChatStates.wait)
async def set_wait_gpt(message: types.Message) -> None:
    await message.answer("Дождитесь обработки предыдущего запроса.")


