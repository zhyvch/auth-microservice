from dataclasses import dataclass

from domain.entities.users import UserCredentialsEntity
from domain.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    user_credentials: UserCredentialsEntity


@dataclass
class UserCredentialsCreatedEvent(BaseEvent):
    user_credentials: UserCredentialsEntity
