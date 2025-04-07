from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from punq import Container

from application.api.auth.schemas import LoginSchema, TokenPairSchema
from domain.entities.tokens import TokenEntity
from infrastructure.auth.jwt import verify_token, create_token_pair
from infrastructure.repositories.users.base import BaseUserCredentialsRepository
from settings.container import initialize_container

router = APIRouter(tags=['Auth'])

security = HTTPBearer()


async def get_token_entity(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenEntity:
    return verify_token(credentials.credentials)


@router.post('/token/login')
async def login(
        schema: LoginSchema,
        container: Annotated[Container, Depends(initialize_container)],
) -> TokenPairSchema:
    repo = container.resolve(BaseUserCredentialsRepository)
    user_credentials = await repo.get(email=schema.email, password=schema.password)
    if not user_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        )

    access_token, refresh_token = create_token_pair(user_credentials.user_id)

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)
