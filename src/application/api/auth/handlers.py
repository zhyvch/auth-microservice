from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from application.api.auth.schemas import LoginSchema, TokenPairSchema, RefreshTokenSchema
from domain.entities.tokens import TokenType, TokenEntity
from infrastrusture.security.crypt import verify_password
from infrastrusture.models import UserCredentials
from infrastrusture.security.jwt import create_jwt, create_token_pair, verify_refresh
from settings.config import settings

router = APIRouter()



@router.post('/token/login')
async def login(schema: LoginSchema) -> TokenPairSchema:
    user = await UserCredentials.find_one({'email': schema.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if not verify_password(schema.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access, refresh = create_token_pair(user.user_id)

    return TokenPairSchema(access_token=access, refresh_token=refresh)


@router.post('/token/refresh')
async def refresh_token(request: RefreshTokenSchema) -> TokenPairSchema:
    token = verify_refresh(request.refresh_token)

    user_creds = await UserCredentials.find_one({'user_id': token.user_id})
    if not user_creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access, refresh = create_token_pair(token.user_id)

    return TokenPairSchema(access_token=access, refresh_token=refresh)
