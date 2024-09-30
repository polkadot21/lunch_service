from pydantic import Extra, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Postgres(BaseSettings):
    driver: str = "postgresql+asyncpg"
    host: str = Field("localhost", alias="LS_POSTGRES_HOST")
    port: int = 5432
    username: str = Field(..., alias="LS_POSTGRES_USERNAME")
    password: SecretStr = Field(..., alias="LS_POSTGRES_PASSWORD")
    database: str = Field("lunch_service_db", alias="LS_POSTGRES_DATABASE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LS_POSTGRES_",
        env_file_encoding="utf-8",
        extra=Extra.ignore,
    )


class SuperUser(BaseSettings):
    username: str = Field(..., alias="SUPERUSER_USERNAME")
    email: str = Field(..., alias="SUPERUSER_EMAIL")
    password: SecretStr = Field(..., alias="SUPERUSER_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SUPERUSER_",
        env_file_encoding="utf-8",
        extra=Extra.ignore,
    )


class Settings(BaseSettings):
    db: Postgres = Postgres()  # type: ignore
    superuser: SuperUser = SuperUser()  # type: ignore

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra=Extra.ignore
    )


# Create an instance of Settings to load environment variables
settings = Settings()
