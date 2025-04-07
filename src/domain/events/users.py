from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from domain.events.base import BaseEvent


class UserCredentialsStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


@dataclass
class UserCredentialsCreatedEvent(BaseEvent):
    user_id: UUID
    status: UserCredentialsStatus
