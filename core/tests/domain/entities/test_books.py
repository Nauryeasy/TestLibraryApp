import pytest
import faker

from core.domain.entities.books import Book
from core.domain.values.books import Title, Author, Year, Status


def test_create_book_success():

    title = Title(faker.Faker().text(max_nb_chars=100))
    author = Author(faker.Faker().text(max_nb_chars=100))
    year = Year(faker.Faker().year())
    status = Status(True)

    book = Book(title, author, year)

    assert book.title.as_generic_type() == title.as_generic_type()
    assert book.author.as_generic_type() == author.as_generic_type()
    assert book.year == year
    assert book.status.as_generic_type() == status.as_generic_type()
    assert book.title == title
    assert book.author == author
    assert book.status == status
    assert book == book
