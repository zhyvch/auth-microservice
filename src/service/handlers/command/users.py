from dataclasses import dataclass

from domain.commands.users import CreateUserCredentialsCommand, UpdateUserCredentialsCommand
from domain.events.users import UserCredentialsCreatedEvent
from service.handlers.command.base import BaseCommandHandler
from service.units_of_work.users.base import BaseUserCredentialsUnitOfWork


@dataclass
class CreateUserCredentialsCommandHandler(BaseCommandHandler):
    uow: BaseUserCredentialsUnitOfWork

    async def __call__(self, command: CreateUserCredentialsCommand) -> None:
        async with self.uow:
            await self.uow.user_credentials.add(command.user_credentials)
            command.user_credentials.events.append(UserCredentialsCreatedEvent(command.user_credentials))
            await self.uow.commit()


@dataclass
class UpdateUserCredentialsCommandHandler(BaseCommandHandler):
    uow: BaseUserCredentialsUnitOfWork

    async def __call__(self, command: UpdateUserCredentialsCommand) -> None:
        ...
