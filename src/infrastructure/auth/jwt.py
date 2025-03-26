from datetime import datetime, timezone, timedelta
from functools import lru_cache
from typing import Dict, Any
from uuid import UUID

import jwt
from fastapi import HTTPException, status

from domain.entities.tokens import TokenEntity, TokenType
from domain.entities.users import UserCredentialsEntity
from infrastructure.auth.security import get_private_key, get_public_key
from settings.config import settings


PRIVATE_KEY = get_private_key()
PUBLIC_KEY = get_public_key()


def sign_payload(token: TokenEntity) -> str:
    payload = {
        'jti': str(token.id),
        'sub': str(token.user_id),
        'exp': int(token.expires_at.timestamp()),
        'iat': int(token.created_at.timestamp()),
        'type': token.type.value,
    }

    signed_payload = jwt.encode(
        payload=payload,
        key=PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return signed_payload

def create_token_pair(user_id: UUID) -> (str, str):
    now = datetime.now(timezone.utc)
    access = sign_payload(
        TokenEntity(
            user_id=user_id,
            type=TokenType.ACCESS,
            expires_at=now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        )
    )
    refresh = sign_payload(
        TokenEntity(
            user_id=user_id,
            type=TokenType.REFRESH,
            expires_at=now + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES),
        )
    )

    return access, refresh


def verify_token(token: str) -> TokenEntity:
    try:
        payload = jwt.decode(
            jwt=token,
            key=PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token = TokenEntity(
            id=UUID(payload['jti']),
            user_id=UUID(payload['sub']),
            expires_at=datetime.fromtimestamp(payload['exp'], tz=timezone.utc),
            created_at=datetime.fromtimestamp(payload['iat'], tz=timezone.utc),
            type=TokenType(payload['type']),
        )

        if datetime.now(timezone.utc) > token.expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return token
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

