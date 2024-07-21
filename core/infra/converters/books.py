from core.domain.entities.books import Book
from core.domain.values.books import Title, Author, Year, Status


"""Методы для конвертации данных между сущностями и документами."""


def convert_book_to_document(book: Book) -> dict:
    return {
        'oid': book.oid,
        'title': book.title.as_generic_type(),
        'author': book.author.as_generic_type(),
        'year': book.year.as_generic_type(),
        'status': book.status.as_generic_type()
    }


def convert_document_to_book(document: dict) -> Book:
    return Book(
        oid=document['oid'],
        title=Title(document['title']),
        author=Author(document['author']),
        year=Year(document['year']),
        status=Status(document['status'])
    )
