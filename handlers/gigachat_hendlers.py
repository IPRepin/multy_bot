from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from giga_chat.generators_gigachat import get_gigachat_text
from keyboards.gigachat_keyboards.gigachat_replay_keyboards import get_gigachat_keyboard
from keyboards.replay_keyboards import get_main_keyboard
from utils.states import ChatStates

gigachat_router = Router()


@gigachat_router.message(F.text.in_(["Новый запрос", "🤖Нейро помошник маркеторлога"]))
async def get_chatting(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ChatStates.text)
    if message.text == "🤖Нейро помошник маркеторлога":
        await message.answer('Введите ваш запрос. Например "Что ты умеешь?"')
    else:
        await message.answer("Введите новый запрос.")


@gigachat_router.message(ChatStates.text)
async def get_chat_response(message: types.Message, state: FSMContext) -> None:
    gpt_answer = await get_gigachat_text(message.text)
    await state.set_state(ChatStates.wait)
    await message.answer(gpt_answer,
                         reply_markup=await get_gigachat_keyboard())
    await state.clear()


@gigachat_router.message(ChatStates.wait)
async def set_wait_gpt(message: types.Message) -> None:
    await message.answer("Дождитесь обработки предыдущего запроса.")


@gigachat_router.message(F.text == "На главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Вы вернулись в главное меню.",
                         reply_markup=await get_main_keyboard())
