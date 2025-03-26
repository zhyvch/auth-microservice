from dataclasses import dataclass

from domain.events.users import UserCredentialsCreatedEvent, UserCreatedEvent
from service.handlers.event.base import BaseEventHandler

@dataclass
class UserCreatedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserCreatedEvent) -> None:
        ...


@dataclass
class UserCredentialsCreatedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserCredentialsCreatedEvent) -> None:
        ...


@dataclass
class SendUserCreatedNotificationEventHandler(BaseEventHandler):
    async def __call__(self, event: UserCredentialsCreatedEvent) -> None:
        ...