from handlers.commands_handler import command_router
from handlers.currency_handlers import currency_router
from handlers.weather_handlers import weather_router


def get_routers():
    return [
        command_router,
        currency_router,
        weather_router,
    ]
