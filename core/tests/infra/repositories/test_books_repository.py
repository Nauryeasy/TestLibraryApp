import pytest
from faker import Faker

from core.domain.entities.books import Book
from core.domain.values.books import Title, Author, Year, Status
from core.infra.filters.books import BookFilters
from core.infra.repositories.base import BaseBooksRepository


def test_add_book(
        books_repository: BaseBooksRepository
):

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )

    books_repository.add_book(book)

    assert book in books_repository.get_books()

    books_repository.clear()


def test_get_books(
        books_repository: BaseBooksRepository
):

    assert not books_repository.get_books()

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    books = books_repository.get_books()

    assert books
    assert len(books) == 1
    assert book in books

    books_repository.clear()


def test_update_book(
        books_repository: BaseBooksRepository
):

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    updated_book = Book(
        oid=book.oid,
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )

    books_repository.update_book(updated_book)

    books = books_repository.get_books()

    assert books[0].oid == updated_book.oid
    assert books[0].title.as_generic_type() == updated_book.title.as_generic_type()
    assert books[0].author.as_generic_type() == updated_book.author.as_generic_type()
    assert books[0].year.as_generic_type() == updated_book.year.as_generic_type()
    assert books[0].status.as_generic_type() == updated_book.status.as_generic_type()

    books_repository.clear()


def test_delete_book(
        books_repository: BaseBooksRepository
):

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    books_repository.delete_book(book.oid)

    books = books_repository.get_books()

    assert book not in books
    assert not books

    books_repository.clear()


def test_get_book_by_oid(
        books_repository: BaseBooksRepository
):

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    found_book = books_repository.get_book_by_oid(book.oid)

    assert found_book
    assert found_book.oid == book.oid
    assert found_book.title.as_generic_type() == book.title.as_generic_type()
    assert found_book.author.as_generic_type() == book.author.as_generic_type()
    assert found_book.year.as_generic_type() == book.year.as_generic_type()
    assert found_book.status.as_generic_type() == book.status.as_generic_type()

    books_repository.clear()


def test_get_books_by_title(
        books_repository: BaseBooksRepository
):
    title = Title(Faker().text(max_nb_chars=100))

    book = Book(
        title=title,
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    found_books = books_repository.get_books(filters=BookFilters(title=title.as_generic_type()))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].title.as_generic_type() == title.as_generic_type()

    found_books = books_repository.get_books(filters=BookFilters(title=title.as_generic_type()[:5]))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].title.as_generic_type() == title.as_generic_type()

    books_repository.clear()


def test_get_books_by_author(
        books_repository: BaseBooksRepository
):
    author = Author(Faker().name())

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=author,
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    found_books = books_repository.get_books(filters=BookFilters(author=author.as_generic_type()))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].author.as_generic_type() == author.as_generic_type()

    found_books = books_repository.get_books(filters=BookFilters(author=author.as_generic_type()[:5]))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].author.as_generic_type() == author.as_generic_type()

    books_repository.clear()


def test_get_books_by_year(
        books_repository: BaseBooksRepository
):
    year = Year(Faker().year())

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=year,
    )
    books_repository.add_book(book)

    found_books = books_repository.get_books(filters=BookFilters(year=year.as_generic_type()))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].year.as_generic_type() == year.as_generic_type()

    books_repository.clear()


def test_get_books_by_status(
        books_repository: BaseBooksRepository
):
    status = Status(True)

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
        status=status
    )
    books_repository.add_book(book)

    found_books = books_repository.get_books(filters=BookFilters(status=status.as_generic_type()))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].status.as_generic_type() == status.as_generic_type()

    books_repository.clear()


def test_get_books_failed(
        books_repository: BaseBooksRepository
):

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    found_books = books_repository.get_books(filters=BookFilters(title='*(&*(&(&(&(&*'))

    assert not found_books


def test_get_books_many_filters(
        books_repository: BaseBooksRepository
):

    book = Book(
        title=Title(Faker().text(max_nb_chars=100)),
        author=Author(Faker().name()),
        year=Year(Faker().year()),
    )
    books_repository.add_book(book)

    found_books = books_repository.get_books(filters=BookFilters(
        title=book.title.as_generic_type(),
        author=book.author.as_generic_type(),
        year=book.year.as_generic_type(),
    ))

    assert found_books
    assert len(found_books) == 1
    assert found_books[0].title.as_generic_type() == book.title.as_generic_type()
    assert found_books[0].author.as_generic_type() == book.author.as_generic_type()
    assert found_books[0].year.as_generic_type() == book.year.as_generic_type()

    books_repository.clear()
