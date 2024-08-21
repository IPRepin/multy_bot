from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    TELEGRAM_TOKEN: str
    LOGS_PATH: str

    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_URL: str

    OPEN_WEATHER_TOKEN: str

    GIGACHAT_AUTHORIZATION: str

    class Config:
        env_file: str = ".env"


settings = Settings()
