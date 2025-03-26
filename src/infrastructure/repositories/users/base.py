from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.users import UserCredentialsEntity


@dataclass
class BaseUserCredentialsRepository(ABC):
    loaded_credentials: set[UserCredentialsEntity] = field(default_factory=set, kw_only=True)

    @abstractmethod
    async def add(self, user_credentials: UserCredentialsEntity) -> None:
        pass

    @abstractmethod
    async def get(self, email: str, password: str) -> UserCredentialsEntity | None:
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        add = cls.add
        get = cls.get

        async def _add(self, user_credentials: UserCredentialsEntity) -> None:
            await add(self, user_credentials)
            self.loaded_users.add(user_credentials)

        async def _get(self, email: str, password: str) -> UserCredentialsEntity | None:
            user = await get(self, email, password)
            if user:
                self.loaded_users.add(user)
            return user

        cls.add = _add
        cls.get = _get
