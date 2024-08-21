from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from giga_chat.generators_gigachat import get_gigachat_text
from utils.states import ChatStates

gigachat_router = Router()


@gigachat_router.message(F.text == "🤖Нейро помошник")
async def get_chatting(message: types.Message, state: FSMContext) -> None:
    await state.set_state(ChatStates.text)
    await message.answer("Введите ваш запрос")


@gigachat_router.message(ChatStates.text)
async def get_chat_response(message: types.Message, state: FSMContext) -> None:
    gpt_answer = await get_gigachat_text(message.text)
    await state.set_state(ChatStates.wait)
    await message.answer(gpt_answer, )
    await state.clear()


@gigachat_router.message(ChatStates.wait)
async def set_wait_gpt(message: types.Message) -> None:
    await message.answer("Дождитесь ответа на предедущий запрос!!!")
