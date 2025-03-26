import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID, DateTime, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import Base

uuid_pk = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True)]
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class UserCredentialsModel(Base):
    __tablename__ = 'user_credentials'

    id: Mapped[uuid_pk]
    created_at: Mapped[timestamp] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_email',
        ),
    )