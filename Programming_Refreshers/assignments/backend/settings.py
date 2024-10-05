from typing import Literal, Optional

from pydantic_settings import BaseSettings

Environments = Literal["dev", "prod", "test", "demo"]
LogLevel = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    environment: Environments = "dev"
    db_schema: Optional[str] = None
    db_name: Optional[str] = "sltech_backend.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"
        str_strip_whitespace = True
        env_nested_delimiter = "__"


settings = Settings()
