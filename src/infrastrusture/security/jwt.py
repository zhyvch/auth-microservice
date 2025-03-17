from datetime import datetime, timezone
from uuid import UUID

import jwt
from fastapi import HTTPException, status

from domain.entities.tokens import TokenEntity, TokenType
from settings.config import settings
from infrastrusture.security.crypt import load_private_key, load_public_key


PRIVATE_KEY = load_private_key()
PUBLIC_KEY = load_public_key()


def create_jwt(token: TokenEntity) -> str:
    payload = {
        'jti': str(token.id),
        'sub': str(token.user_id),
        'exp': token.expires_at,
        'iat': token.created_at,
        'type': token.type.value
    }
    encoded_jwt = jwt.encode(
        payload=payload,
        key=PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def create_token_pair(user_id: UUID) -> (str, str):
    access = create_jwt(
        TokenEntity(
            user_id=user_id,
            type=TokenType.ACCESS,
            expires_at=datetime.now(timezone.utc) + settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    refresh = create_jwt(
        TokenEntity(
            user_id=user_id,
            type=TokenType.REFRESH,
            expires_at=datetime.now(timezone.utc) + settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
        )
    )

    return access, refresh


def verify_refresh(jwt_token: str) -> TokenEntity:
    try:
        payload = jwt.decode(
            jwt=jwt_token,
            key=PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token = TokenEntity(
            id=payload['jti'],
            user_id=datetime.timestamp(payload['sub']),
            expires_at=payload['exp'],
            created_at=payload['iat'],
            type=payload['type'],
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
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )