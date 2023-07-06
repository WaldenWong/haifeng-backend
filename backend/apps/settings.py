#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional, Union

from pydantic import BaseSettings, FilePath, validator

from backend.apps.schemas.db_config import DatabaseURL


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("ALLOWED_HOSTS", "CAPTCHA_FONT_PATHS", pre=True)
    def CommaSeparatedStrings(cls, v: Optional[str]) -> List[str]:  # noqa
        if not v:
            return []
        return [item.strip() for item in v.split(",")]

    @property
    def DATABASE_CONFIG(self) -> DatabaseURL:  # noqa
        return DatabaseURL(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    @property
    def ALEMBIC_CONFIG(self) -> DatabaseURL:  # noqa
        return DatabaseURL(
            drivername="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    # SYSTEM
    TESTING: bool = False
    DEBUG: bool = False
    PROJECT_NAME: str = "haifeng"
    DATA_PATH: str = f"/tmp/{PROJECT_NAME}/"

    IDE: str = "dev"
    SECRET_KEY: Optional[str] = None

    TOKEN_URL: str = "/token"
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 60 * 240

    # FASTAPI
    SAME_SITE: Optional[str] = None
    ALLOWED_HOSTS: Optional[Union[str, List[str]]] = None

    # DATABASE
    DB_NAME: str = "default"
    DB_USER: str = "default"
    DB_PASSWORD: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_ECHO_LOG: bool = False
    DB_ECHO_LEVEL: str = "error"

    # USER AUTH
    CRYPT_SCHEMA: str = "bcrypt"
    CAPTCHA_FONT_PATHS: Union[None, str, List[FilePath]] = None

    # REDIS
    NODE_BACKEND_URL: str = "redis://127.0.0.1:6379"

    # RABBITMQ
    NODE_BROKER_URL: str = "amqp://127.0.0.1:5672/?heartbeat=120"


settings = Settings()
