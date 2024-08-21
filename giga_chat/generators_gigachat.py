import re
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole, Image
# from aiofile import async_open
from config import settings


async def get_gigachat_text(bot_message: str) -> str:
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.USER,
                content=bot_message
            )
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    async with GigaChat(credentials=settings.GIGACHAT_AUTHORIZATION, verify_ssl_certs=False) as giga:
        response = giga.chat(payload)
        return response.choices[0].message.content


async def get_gigachat_image(msg: str) -> str:
    payload = Chat(
        messages=[Messages(role=MessagesRole.USER, content=msg)],
        temperature=0.7,
        max_tokens=1000,
        function_call="auto",
    )
    async with GigaChat(credentials=settings.GIGACHAT_AUTHORIZATION, verify_ssl_certs=False) as giga:
        response = giga.chat(payload)
        text = response.choices[0].message.content
        match = re.search(r'src="([^"]+)"', text)
        image: Image = await giga.aget_image(file_id=match.group(1))
