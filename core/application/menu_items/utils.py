from core.domain.entities.books import Book


def print_book(book: Book):
    print()
    print(f'ID: {book.oid}')
    print(f'Название: {book.title.as_generic_type()}')
    print(f'Автор: {book.author.as_generic_type()}')
    print(f'Год издания: {book.year.as_generic_type()}')
    print(f'Статус: {status_to_str(book.status.as_generic_type())}')
    print()


def status_to_str(status: bool) -> str:
    return 'В наличии' if status else 'Нет в наличии'
