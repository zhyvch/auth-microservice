from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.value_objects.users import EmailVO


@dataclass(eq=False)
class UserCredentialsEntity(BaseEntity):
    user_id: UUID
    email: EmailVO
    hashed_password: str
