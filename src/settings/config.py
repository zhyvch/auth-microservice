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

    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_USER: str
    MONGODB_PASSWORD: str

    @property
    def MONGODB_URL(self):
        return f'mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}/'

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        case_sensitive=True
    )

settings = Settings()
