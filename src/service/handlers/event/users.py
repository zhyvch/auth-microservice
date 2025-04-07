from dataclasses import dataclass


from domain.events.users import UserCredentialsCreatedEvent
from service.handlers.event.base import BaseEventHandler


@dataclass
class UserCredentialsCreatedEventHandler(BaseEventHandler):
    async def __call__(self, event: UserCredentialsCreatedEvent) -> None:
        await self.producer.publish(event, self.topic)
