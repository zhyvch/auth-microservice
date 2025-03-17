from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4, UUID


@dataclass
class BaseEntity(ABC):
    id: UUID = field(
        default_factory=lambda: uuid4,
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id
