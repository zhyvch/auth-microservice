from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class EmailIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Email is empty'


@dataclass(frozen=True, eq=False)
class EmailTooShortException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> is too short'


@dataclass(frozen=True, eq=False)
class EmailTooLongException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email[255:]}...> is too long'


@dataclass(frozen=True, eq=False)
class EmailNotContainingAtSymbolException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> must contain an "@" symbol'


@dataclass(frozen=True, eq=False)
class PasswordIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password is empty'


@dataclass(frozen=True, eq=False)
class PasswordTooShortException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password is too short'


@dataclass(frozen=True, eq=False)
class PasswordTooLongException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password is too long'


@dataclass(frozen=True, eq=False)
class PasswordNotContainingDigitsException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password must contain at least one digit'


@dataclass(frozen=True, eq=False)
class PasswordNotContainingCapitalLetterException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password must contain at least one capital letter'


@dataclass(frozen=True, eq=False)
class PasswordNotContainingSpecialSymbolException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password must contain at least special symbol (e.g. !@#$%^&*()-_=+[]{}|;:,.<>?/~` )'
