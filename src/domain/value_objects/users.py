# TODO: Move validation to a separate class
from dataclasses import dataclass

from domain.exceptions.users import (
    EmailIsEmptyException,
    EmailTooShortException,
    EmailTooLongException,
    EmailNotContainingAtSymbolException,
    PasswordIsEmptyException,
    PasswordTooShortException,
    PasswordTooLongException,
    PasswordNotContainingDigitsException,
    PasswordNotContainingCapitalLetterException,
    PasswordNotContainingSpecialSymbolException,
)
from domain.value_objects.base import BaseVO


@dataclass(frozen=True)
class EmailVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not self.value:
            raise EmailIsEmptyException()

        if len(self.value) < 5:
            raise EmailTooShortException(self.value)

        if len(self.value) > 255:
            raise EmailTooLongException(self.value)

        if '@' not in self.value:
            raise EmailNotContainingAtSymbolException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class str(BaseVO):
    value: str

    def validate(self) -> bool:
        if not self.value:
            raise PasswordIsEmptyException()

        if len(self.value) < 10:
            raise PasswordTooShortException()

        if len(self.value) > 255:
            raise PasswordTooLongException()

        if not any(char.isdigit() for char in self.value):
            raise PasswordNotContainingDigitsException()

        if not any(char.isupper() for char in self.value):
            raise PasswordNotContainingCapitalLetterException()

        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~`' for char in self.value):
            raise PasswordNotContainingSpecialSymbolException()

        return True

    def as_generic(self) -> str:
        return str(self.value)