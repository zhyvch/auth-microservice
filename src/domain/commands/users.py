from dataclasses import dataclass

from domain.commands.base import BaseCommand
from domain.entities.users import UserCredentialsEntity


@dataclass
class CreateUserCredentialsCommand(BaseCommand):
    user_credentials: UserCredentialsEntity


@dataclass
class UpdateUserCredentialsCommand(BaseCommand):
    user_credentials: UserCredentialsEntity
