import pytest

from core.domain.entities.books import Book
from core.domain.values.books import Title, Author, Year, Status
from core.infra.converters.books import convert_document_to_book, convert_book_to_document


def test_convert_document_to_book():
    document = {
        'oid': '123',
        'title': 'title',
        'author': 'author',
        'year': '2020',
        'status': True
    }

    book = convert_document_to_book(document)

    assert book.oid == document['oid']
    assert book.title.as_generic_type() == document['title']
    assert book.author.as_generic_type() == document['author']
    assert book.year.as_generic_type() == document['year']
    assert book.status.as_generic_type() == document['status']
    assert document == convert_book_to_document(book)


def test_convert_book_to_document():
    book = Book(Title('title'), Author('author'), Year('2020'), Status(True))

    document = convert_book_to_document(book)

    assert document['oid'] == book.oid
    assert document['title'] == book.title.as_generic_type()
    assert document['author'] == book.author.as_generic_type()
    assert document['year'] == book.year.as_generic_type()
    assert document['status'] == book.status.as_generic_type()
    assert book == convert_document_to_book(document)
