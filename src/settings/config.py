from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent

    AUTH_SERVICE_API_PORT: int
    AUTH_SERVICE_DEBUG: bool

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    JWT_ALGORITHM: str = 'RS256'

    RSA_PRIVATE_KEY_PATH: Path = BASE_PATH / 'keys/private.pem'
    RSA_PUBLIC_KEY_PATH: Path = BASE_PATH / 'keys/public.pem'

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: int
    RABBITMQ_VHOST: str
    RABBITMQ_PORT: int

    @property
    def POSTGRES_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        case_sensitive=True
    )


settings = Settings()
