from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity


@dataclass(eq=False)
class UserCredentials(BaseEntity):
    user_id: UUID
    email: str
    hashed_password: str
