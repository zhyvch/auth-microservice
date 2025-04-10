import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Union

from domain.commands.base import BaseCommand
from domain.events.base import BaseEvent
from service.handlers.command.base import BaseCommandHandler
from service.handlers.event.base import BaseEventHandler
from service.units_of_work.users.base import BaseUserCredentialsUnitOfWork

logger = logging.getLogger(__name__)

Message = Union[BaseEvent, BaseCommand]


@dataclass
class MessageBus:
    uow: BaseUserCredentialsUnitOfWork
    commands_map: dict[type[BaseCommand], BaseCommandHandler] = field(
        default_factory=dict,
        kw_only=True,
    )
    events_map: dict[type[BaseEvent], list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queue: list[Message] = field(
        default_factory=list,
        kw_only=True,
    )

    async def handle(self, message: Message):
        self.queue.append(message)
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, BaseCommand):
                await self.handle_command(message)
            elif isinstance(message, BaseEvent):
                await self.handle_event(message)
            else:
                raise Exception(f'{message} was not an Event or Command')

    async def handle_command(self, command: BaseCommand):
        logger.debug('handling command %s', command)
        try:
            handler = self.commands_map[command.__class__]
            await handler(command)
            self.queue.extend(self.uow.collect_new_event())
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise

    async def handle_event(self, event: BaseEvent):
        for handler in self.events_map[event.__class__]:
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                await handler(event)
                self.queue.extend(self.uow.collect_new_event())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue
