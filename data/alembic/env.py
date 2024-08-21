import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from config import settings
from data.models import BaseModelBot

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModelBot.metadata


def run_migrations_online() -> None:
    connectable = create_async_engine(settings.DB_URL)

    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    async def async_main():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(async_main())


if context.is_offline_mode():
    def run_migrations_offline() -> None:
        context.configure(url=settings.DB_URL, target_metadata=target_metadata, literal_binds=True)
        with context.begin_transaction():
            context.run_migrations()


    run_migrations_offline()
else:
    run_migrations_online()
