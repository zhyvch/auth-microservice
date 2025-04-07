from dataclasses import dataclass
from uuid import UUID

from application.external_events.handlers.base import BaseExternalEventHandler
from domain.commands.users import CreateUserCredentialsCommand
from domain.entities.users import UserCredentialsEntity
from domain.value_objects.users import EmailVO
from infrastructure.auth.security import hash_password


@dataclass
class UserCreatedExternalEventHandler(BaseExternalEventHandler):
    async def __call__(self, body: dict) -> None:
        user_credentials = UserCredentialsEntity(
            user_id=UUID(body['user_id']),
            email=EmailVO(body['email']),
            hashed_password=hash_password(body['password']),
        )
        await self.bus.handle(CreateUserCredentialsCommand(user_credentials=user_credentials))
