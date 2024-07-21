import pytest
from faker import Faker

from core.domain.entities.books import Book
from core.domain.values.books import Title, Author, Year
from core.infra.exceptions.books import BookNotFoundException
from core.infra.repositories.base import BaseBooksRepository
from core.logic.commands.books import GetBooksCommand, AddBookCommand, UpdateBookStatusCommand, DeleteBookCommand, FindBookCommand
from core.logic.mediator import Mediator


def test_init_mediator(
        mediator: Mediator
):
    assert len(mediator.command_map[GetBooksCommand]) == 1
    assert len(mediator.command_map[AddBookCommand]) == 1
    assert len(mediator.command_map[UpdateBookStatusCommand]) == 1
    assert len(mediator.command_map[DeleteBookCommand]) == 1
    assert len(mediator.command_map[FindBookCommand]) == 1


def test_get_books_command(
    mediator: Mediator,
    books_repository: BaseBooksRepository
):
    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    books, *_ = mediator.handle_command(GetBooksCommand())

    assert book in books
    assert len(books) == 1

    books_repository.clear()


def test_add_book_command(
    mediator: Mediator,
    books_repository: BaseBooksRepository
):

    title = Faker().text(max_nb_chars=100)
    author = Faker().name()
    year = Faker().year()

    mediator.handle_command(AddBookCommand(title, author, year))

    books = books_repository.get_books()

    book = books[0]

    assert len(books) == 1
    assert book.title.as_generic_type() == title
    assert book.author.as_generic_type() == author
    assert book.year.as_generic_type() == year

    books_repository.clear()


def test_update_book_status_command(
    mediator: Mediator,
    books_repository: BaseBooksRepository
):
    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    mediator.handle_command(UpdateBookStatusCommand(book.oid))

    books = books_repository.get_books()

    assert len(books) == 1
    assert books[0].status.as_generic_type() is False

    mediator.handle_command(UpdateBookStatusCommand(book.oid))

    books = books_repository.get_books()

    assert len(books) == 1
    assert books[0].status.as_generic_type() is True

    books_repository.clear()


def test_delete_book_command(
    mediator: Mediator,
    books_repository: BaseBooksRepository
):
    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    mediator.handle_command(DeleteBookCommand(book.oid))

    books = books_repository.get_books()

    assert len(books) == 0

    books_repository.clear()


def test_find_book_command(
    mediator: Mediator,
    books_repository: BaseBooksRepository
):
    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    books, *_ = mediator.handle_command(FindBookCommand(title=book.title.as_generic_type()))

    assert book in books
    assert len(books) == 1

    books_repository.clear()


def test_delete_book_fail(
    mediator: Mediator,
    books_repository: BaseBooksRepository
):
    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    with pytest.raises(BookNotFoundException):
        mediator.handle_command(DeleteBookCommand('test'))

    books = books_repository.get_books()

    assert len(books) == 1

    books_repository.clear()
