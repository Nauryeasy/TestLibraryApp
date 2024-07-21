import json
import os
from typing import Dict, List

from core.domain.entities.books import Book
from core.infra.converters.books import convert_book_to_document, convert_document_to_book
from core.infra.exceptions.books import BookNotFoundException
from core.infra.filters.books import BookFilters
from core.infra.repositories.base import BaseBooksRepository


"""Реализация репозитория для книг для хранения в json"""


class MemoryJsonBooksRepository(BaseBooksRepository):

    data: dict = None

    def __init__(self, path_to_file: str) -> None:
        self.path_to_file = path_to_file
        self.data: Dict[str, dict] = {}
        self._ensure_file_exists()

    @staticmethod
    def _build_query_filters(filters: BookFilters) -> lambda book: bool:
        """Функция для создания lambda функции для использования в filter в get_books"""
        return lambda book: (filters.title is None or filters.title.lower() in book.title.as_generic_type().lower()) and \
               (filters.author is None or filters.author.lower() in book.author.as_generic_type().lower()) and \
               (filters.year is None or book.year.as_generic_type() == filters.year) and \
               (filters.status is None or book.status.as_generic_type() == filters.status)

    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self.path_to_file):
            with open(self.path_to_file, 'w') as file:
                json.dump({}, file)

    """load and save data для того, чтобы не хранить все книги в оперативной памяти"""
    def _load_data(self) -> None:
        with open(self.path_to_file, 'r+') as file:
            try:
                self.data = json.load(file)
            except json.JSONDecodeError:
                self.data = {}

    def _save_data(self) -> None:
        with open(self.path_to_file, 'w') as file:
            json.dump(self.data, file, indent=4)
        self.data = {}

    def get_books(self, filters: BookFilters | None = None) -> List[Book]:
        self._load_data()

        books = [convert_document_to_book(book) for book in self.data.values()]

        if filters:
            query = self._build_query_filters(filters)
            books = list(filter(query, books))

        self._save_data()

        return books

    def add_book(self, book: Book) -> None:
        self._load_data()

        book_document = convert_book_to_document(book)
        self.data[book_document['oid']] = book_document

        self._save_data()

    def update_book(self, book: Book) -> None:
        self._load_data()

        book_document = convert_book_to_document(book)
        if book_document['oid'] not in self.data:
            raise BookNotFoundException(book_document['oid'])

        self.data[book_document['oid']] = book_document

        self._save_data()

    def delete_book(self, oid: str) -> None:
        self._load_data()

        if oid not in self.data:
            raise BookNotFoundException(oid)

        del self.data[oid]

        self._save_data()

    def get_book_by_oid(self, oid: str) -> Book:
        self._load_data()

        if oid not in self.data:
            raise BookNotFoundException(oid)

        book = convert_document_to_book(self.data[oid])

        self._save_data()

        return book

    def clear(self) -> None:
        """Метод для очистки репозитория. Необходим для тестирования"""
        self.data = {}
        self._save_data()
