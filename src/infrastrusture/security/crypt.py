import pathlib

from passlib.context import CryptContext
from settings.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def load_private_key() -> bytes:
    with open(settings.RSA_PRIVATE_KEY_PATH, 'rb') as f:
        return f.read()


def load_public_key() -> bytes:
    with open(settings.RSA_PUBLIC_KEY_PATH, 'rb') as f:
        return f.read()
