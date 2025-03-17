from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

from domain.entities.base import BaseEntity


class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


@dataclass(eq=False)
class TokenEntity(BaseEntity):
    user_id: UUID
    type: TokenType
    expires_at: datetime
