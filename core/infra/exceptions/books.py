from dataclasses import dataclass

from core.infra.exceptions.base import InfrastructureException


@dataclass(eq=False)
class BookNotFoundException(InfrastructureException):
    book_oid: str

    @property
    def message(self) -> str:
        return f'Book with oid "{self.book_oid}" not found'
