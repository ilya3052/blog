from pathlib import Path

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, TomlConfigSettingsSource, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class DjangoSecretConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding="utf-8",
        env_prefix="DJANGO_",
        extra="ignore",
        case_sensitive=False
    )
    secret_key: SecretStr


class DatabaseSecretConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding="utf-8",
        env_prefix="DB_",
        extra="ignore",
        case_sensitive=False
    )
    password: SecretStr


class SecretRedisConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
        extra="ignore",
        case_sensitive=False
    )
    password: SecretStr


class RedisConfig(BaseModel):
    host: str
    port: int
    channel: str


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    name: str


class Config(BaseSettings):
    database: DatabaseConfig
    secret_database: DatabaseSecretConfig = Field(default_factory=DatabaseSecretConfig)
    redis: RedisConfig
    secret_redis: SecretRedisConfig = Field(default_factory=SecretRedisConfig)
    secret_django: DjangoSecretConfig = Field(default_factory=DjangoSecretConfig)

    @classmethod
    def load(cls) -> 'Config':
        return cls()

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        return (TomlConfigSettingsSource(settings_cls, BASE_DIR / 'config.toml'),)
