"""Пример работы с чатом через gigachain"""
import logging

from langchain_community.chat_models.gigachat import GigaChat
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage

from config import settings

logger = logging.getLogger(__name__)

async def get_connection():
    llm = GigaChat(credentials=settings.GIGACHAT_AUTHORIZATION,
                    verify_ssl_certs=False)
    chat = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory(),
    )

    return chat


async def get_gigachat_text(bot_message: str) -> str:
    messages = [
        SystemMessage(
            content="Ты опытный интернет маркетолог разбираешься во множестве"
                    "инструментов таких как: яндекс директ, яндекс метрика,"
                    "VK target, MyTarget. Можешь грамотно написать продающие тексты для "
                    "объявлений. Способен написать оптимальные SEO тексты. "
                    "Твоя задача помогать другим маркетологам с настройкой рекламных компаний "
                    "анализом рынка, написанием текстов для объявлений, и статей,"
                    " максимально подробно отвечать на вопросы, подкреплять свои ответы "
                    "ссылками на материалы, документацию и видео по теме вопроса."
                    "На все вопросы давай полные, развернутые ответы."
        )
    ]
    chat = await get_connection()
    while True:
        if bot_message == "💬Новый запрос":
            break
        messages.append(HumanMessage(content=bot_message))
        chat.invoke(messages)
        bot_answer = chat.memory.chat_memory.messages[-1].content
        return bot_answer
