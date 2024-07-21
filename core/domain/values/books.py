from dataclasses import dataclass
from datetime import datetime

from core.domain.exceptions.books import (
    BookTitleTooShortException,
    BookTitleTooLongException,
    BookTitleIsEmptyException,
    BookAuthorIsEmptyException,
    BookAuthorTooLongException,
    BookAuthorTooShortException, BookYearIsEmptyException, BookYearNotNumericException,
    BookYearMoreThanCurrentYearException, BookYearMustBeFourDigitsException, BookStatusIsEmptyException,
    BookStatusMustBeBooleanException
)
from core.domain.values.base import BaseValueObject, VT


"""Значения для книг"""


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise BookTitleIsEmptyException()

        if len(self.value) < 3:
            raise BookTitleTooShortException(self.value)

        if len(self.value) > 100:
            raise BookTitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Author(BaseValueObject[str]):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise BookAuthorIsEmptyException()

        if len(self.value) < 3:
            raise BookAuthorTooShortException(self.value)

        if len(self.value) > 100:
            raise BookAuthorTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Year(BaseValueObject[str]):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise BookYearIsEmptyException()

        if not self.value.isnumeric():
            raise BookYearNotNumericException(self.value)

        if int(self.value) > datetime.now().year:
            raise BookYearMoreThanCurrentYearException(self.value)

        if len(self.value) != 4:
            raise BookYearMustBeFourDigitsException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)

    def __gt__(self, other: 'Year') -> bool:
        return int(self.value) > int(other.value)

    def __lt__(self, other: 'Year') -> bool:
        return int(self.value) < int(other.value)

    def __eq__(self, other: 'Year') -> bool:
        return int(self.value) == int(other.value)


@dataclass(frozen=True)
class Status(BaseValueObject[bool]):
    value: bool

    def validate(self) -> None:
        if self.value is None:
            raise BookStatusIsEmptyException()

        if not isinstance(self.value, bool):
            raise BookStatusMustBeBooleanException(self.value)

    def as_generic_type(self) -> bool:
        return bool(self.value)
