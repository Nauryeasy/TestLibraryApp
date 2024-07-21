from abc import ABC, abstractmethod
from typing import List

from core.domain.entities.books import Book
from core.infra.filters.books import BookFilters


"""Абстрактная реализация репозитория книг"""


class BaseBooksRepository(ABC):

    @abstractmethod
    def get_books(self, filters: BookFilters = None) -> List[Book]:
        ...

    @abstractmethod
    def add_book(self, book: Book) -> None:
        ...

    @abstractmethod
    def update_book(self, book: Book) -> None:
        ...

    @abstractmethod
    def delete_book(self, oid: str) -> None:
        ...

    @abstractmethod
    def get_book_by_oid(self, oid: str) -> Book:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...
