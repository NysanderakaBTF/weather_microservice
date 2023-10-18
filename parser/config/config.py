import os

from pydantic.config import BaseConfig


class Config(BaseConfig):
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROCKER")
    CELERY_BACKEND_URL: str = os.getenv("CELERY_BACKEND")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")

    OPENWEATHERMAP_KEY: str = os.getenv("OPENWEATHERMAP_KEY")


config = Config()
