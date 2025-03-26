from functools import lru_cache

from punq import Container, Scope

from domain.commands.users import CreateUserCredentialsCommand
from domain.events.users import UserCredentialsCreatedEvent, UserCreatedEvent
from infrastructure.database import session_factory
from infrastructure.repositories.users.base import BaseUserCredentialsRepository
from infrastructure.repositories.users.postgresql import SQLAlchemyUserCredentialsRepository
from service.handlers.command.users import CreateUserCredentialsCommandHandler
from service.handlers.event.users import UserCredentialsCreatedEventHandler, UserCreatedEventHandler
from service.message_bus import MessageBus
from service.units_of_work.users.base import BaseUserCredentialsUnitOfWork
from service.units_of_work.users.postgresql import SQLAlchemyUserCredentialsUnitOfWork
from settings.config import Settings


@lru_cache(1)
def initialize_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()


    def initialize_user_creds_sqlalchemy_repo() -> BaseUserCredentialsRepository:
        return SQLAlchemyUserCredentialsRepository(session_factory())

    container.register(BaseUserCredentialsRepository, factory=initialize_user_creds_sqlalchemy_repo)

    def initialize_user_creds_sqlalchemy_uow() -> BaseUserCredentialsUnitOfWork:
        return SQLAlchemyUserCredentialsUnitOfWork()

    container.register(BaseUserCredentialsUnitOfWork, factory=initialize_user_creds_sqlalchemy_uow)

    def initialize_message_bus() -> MessageBus:
        uow = container.resolve(BaseUserCredentialsUnitOfWork)

        create_user_handler = CreateUserCredentialsCommandHandler(
            uow=uow,
        )

        user_created_handler = UserCreatedEventHandler(

        )

        user_credentials_created_handler = UserCredentialsCreatedEventHandler(

        )

        commands_map = {
            CreateUserCredentialsCommand: create_user_handler,
        }
        events_map = {
            UserCreatedEvent: [user_created_handler],
            UserCredentialsCreatedEvent: [user_credentials_created_handler],
        }

        bus = MessageBus(
            uow=container.resolve(BaseUserCredentialsUnitOfWork),
            commands_map=commands_map,
            events_map=events_map,
        )

        return bus

    container.register(MessageBus, factory=initialize_message_bus, scope=Scope.singleton)


    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    return container
