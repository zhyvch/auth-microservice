from functools import lru_cache

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from passlib.context import CryptContext

from settings.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@lru_cache(1)
def get_private_key() -> RSAPrivateKey:
    with open(settings.RSA_PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
        return private_key


@lru_cache(1)
def get_public_key() -> RSAPublicKey:
    with open(settings.RSA_PUBLIC_KEY_PATH, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
        return public_key
