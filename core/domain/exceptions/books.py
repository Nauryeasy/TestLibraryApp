from dataclasses import dataclass

from core.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class BookTitleTooShortException(ApplicationException):
    title: str

    @property
    def message(self) -> str:
        return f'Title must be at least 3 characters long: "{self.title}"'


@dataclass(eq=False)
class BookTitleTooLongException(ApplicationException):
    title: str

    @property
    def message(self) -> str:
        return f'Title must be at most 100 characters long: "{self.title}"'


@dataclass(eq=False)
class BookTitleIsEmptyException(ApplicationException):

    @property
    def message(self) -> str:
        return f'Title must not be empty'


@dataclass(eq=False)
class BookAuthorTooShortException(ApplicationException):
    title: str

    @property
    def message(self) -> str:
        return f'Title must be at least 3 characters long: "{self.title}"'


@dataclass(eq=False)
class BookAuthorTooLongException(ApplicationException):
    title: str

    @property
    def message(self) -> str:
        return f'Title must be at most 100 characters long: "{self.title}"'


@dataclass(eq=False)
class BookAuthorIsEmptyException(ApplicationException):

    @property
    def message(self) -> str:
        return f'Title must not be empty'


@dataclass(eq=False)
class BookYearIsEmptyException(ApplicationException):

    @property
    def message(self) -> str:
        return f'Year must not be empty'


@dataclass(eq=False)
class BookYearNotNumericException(ApplicationException):
    year: str

    @property
    def message(self) -> str:
        return f'Year must be numeric: "{self.year}"'


@dataclass(eq=False)
class BookYearMoreThanCurrentYearException(ApplicationException):
    year: str

    @property
    def message(self) -> str:
        return f'The year must be less than or equal to the current year: "{self.year}"'


@dataclass(eq=False)
class BookYearMustBeFourDigitsException(ApplicationException):
    year: str

    @property
    def message(self) -> str:
        return f'The year must have four digits: "{self.year}"'


@dataclass(eq=False)
class BookStatusIsEmptyException(ApplicationException):

    @property
    def message(self) -> str:
        return f'The status must not be empty'


@dataclass(eq=False)
class BookStatusMustBeBooleanException(ApplicationException):
    status: bool

    @property
    def message(self) -> str:
        return f'The status must be boolean: "{self.status}"'
