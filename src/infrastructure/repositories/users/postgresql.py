from dataclasses import dataclass

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserCredentialsEntity
from infrastructure.auth.security import verify_password
from infrastructure.converters.users import convert_user_entity_to_model, convert_user_model_to_entity
from infrastructure.models.users import UserCredentialsModel
from infrastructure.repositories.users.base import BaseUserCredentialsRepository


@dataclass
class SQLAlchemyUserCredentialsRepository(BaseUserCredentialsRepository):
    session: AsyncSession

    async def get(self, email: str, password: str) -> UserCredentialsEntity | None:
        query = select(UserCredentialsModel).where(UserCredentialsModel.email.ilike(email))

        result = await self.session.execute(query)
        user_creds_model = result.scalar_one_or_none()

        if user_creds_model:
            if not verify_password(password, user_creds_model.hashed_password):
                raise

            user = convert_user_model_to_entity(user_creds_model)
            return user


    async def add(self, user_credentials: UserCredentialsEntity) -> None:
        credentials = convert_user_entity_to_model(user_credentials)
        self.session.add(credentials)
