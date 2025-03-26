from abc import ABC, abstractmethod

from infrastructure.repositories.users.base import BaseUserCredentialsRepository


class BaseUserCredentialsUnitOfWork(ABC):
    user_credentials: BaseUserCredentialsRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    def collect_new_event(self):
        for credentials in self.user_credentials.loaded_credentials:
            while credentials.events:
                yield credentials.events.pop(0)

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...
