from dataclasses import dataclass

from domain.commands.users import CreateUserCredentialsCommand, UpdateUserCredentialsCommand
from domain.events.users import UserCredentialsCreatedEvent, UserCredentialsStatus
from service.handlers.command.base import BaseCommandHandler
from service.units_of_work.users.base import BaseUserCredentialsUnitOfWork


@dataclass
class CreateUserCredentialsCommandHandler(BaseCommandHandler):
    uow: BaseUserCredentialsUnitOfWork

    async def __call__(self, command: CreateUserCredentialsCommand) -> None:
        async with self.uow:
            try:
                await self.uow.user_credentials.add(command.user_credentials)
                command.user_credentials.events.append(
                    UserCredentialsCreatedEvent(
                        user_id=command.user_credentials.user_id,
                        status=UserCredentialsStatus.SUCCESS,
                    )
                )
                await self.uow.commit()
            except Exception:
                command.user_credentials.events.append(
                    UserCredentialsCreatedEvent(
                        user_id=command.user_credentials.user_id,
                        status=UserCredentialsStatus.FAILED,
                    )
                )
                raise


@dataclass
class UpdateUserCredentialsCommandHandler(BaseCommandHandler):
    uow: BaseUserCredentialsUnitOfWork

    async def __call__(self, command: UpdateUserCredentialsCommand) -> None:
        ...
