from uuid import UUID
from beanie import Document
from pydantic import EmailStr


class UserCredentials(Document):
    user_id: UUID
    email: EmailStr
    hashed_password: str

    class Settings:
        name = 'user_credentials'
        indexes = [
            'user_id',
        ]
