from dataclasses import dataclass

from core.domain.entities.books import Book
from core.domain.values.books import Title, Author, Year, Status
from core.infra.filters.books import BookFilters
from core.infra.repositories.base import BaseBooksRepository
from core.logic.commands.base import BaseCommand, BaseCommandHandler


"""Команды для книг, а так же их Handlers"""


@dataclass(frozen=True)
class GetBooksCommand(BaseCommand):
    ...


@dataclass(frozen=True)
class AddBookCommand(BaseCommand):
    title: str
    author: str
    year: str


@dataclass(frozen=True)
class DeleteBookCommand(BaseCommand):
    oid: str


@dataclass(frozen=True)
class FindBookCommand(BaseCommand):
    title: str | None = None
    author: str | None = None
    year: str | None = None


@dataclass(frozen=True)
class UpdateBookStatusCommand(BaseCommand):
    oid: str


@dataclass(frozen=True)
class GetBooksCommandHandler(BaseCommandHandler[GetBooksCommand, list[Book]]):
    book_repository: BaseBooksRepository

    def handle(self, command: GetBooksCommand) -> list[Book]:
        return self.book_repository.get_books()


@dataclass(frozen=True)
class AddBookCommandHandler(BaseCommandHandler[AddBookCommand, Book]):
    book_repository: BaseBooksRepository

    def handle(self, command: AddBookCommand) -> Book:
        new_book = Book(
            title=Title(command.title),
            author=Author(command.author),
            year=Year(command.year),
        )

        self.book_repository.add_book(new_book)

        return new_book


@dataclass(frozen=True)
class DeleteBookCommandHandler(BaseCommandHandler[DeleteBookCommand, None]):
    book_repository: BaseBooksRepository

    def handle(self, command: DeleteBookCommand) -> None:
        self.book_repository.delete_book(command.oid)


@dataclass(frozen=True)
class FindBookCommandHandler(BaseCommandHandler[FindBookCommand, list[Book]]):
    book_repository: BaseBooksRepository

    def handle(self, command: FindBookCommand) -> list[Book]:
        filters = BookFilters(
            title=command.title,
            author=command.author,
            year=command.year
        )

        return self.book_repository.get_books(filters=filters)


@dataclass(frozen=True)
class UpdateBookStatusCommandHandler(BaseCommandHandler[UpdateBookStatusCommand, Book]):
    book_repository: BaseBooksRepository

    def handle(self, command: UpdateBookStatusCommand) -> Book:
        book = self.book_repository.get_book_by_oid(command.oid)
        book.status = Status(not book.status.as_generic_type())

        self.book_repository.update_book(book)

        return book
