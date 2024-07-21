from typing import Type, TypeVar

from punq import Container

from core.application.menu_items.base import BaseMenuItem
from core.application.menu_items.exceptions import ToMainMenuException
from core.domain.entities.books import Book
from core.domain.values.base import BaseValueObject
from core.domain.values.books import Title, Author, Year
from core.infra.exceptions.books import BookNotFoundException
from core.logic.commands.books import GetBooksCommand, AddBookCommand, DeleteBookCommand, FindBookCommand, \
    UpdateBookStatusCommand
from core.logic.container import init_container
from core.logic.mediator import Mediator
from core.domain.exceptions.books import (
    BookTitleTooShortException,
    BookTitleTooLongException,
    BookTitleIsEmptyException,
    BookAuthorIsEmptyException,
    BookAuthorTooLongException,
    BookAuthorTooShortException,
    BookYearIsEmptyException,
    BookYearNotNumericException,
    BookYearMoreThanCurrentYearException,
    BookYearMustBeFourDigitsException,
)

from core.application.menu_items.utils import print_book


"""Классы, представляющие элементы меню приложения"""


BT = TypeVar('BT', bound=BaseValueObject)


class GetBooksMenuItem(BaseMenuItem):

    def handle(self) -> None:
        container: Container = init_container()
        mediator: Mediator = container.resolve(Mediator)

        books, *_ = mediator.handle_command(GetBooksCommand())

        for book in books:
            print_book(book)

    def to_str_for_menu(self):
        return 'Просмотреть все книги'


class AddBookMenuItem(BaseMenuItem):

    def handle(self) -> None:
        container: Container = init_container()
        mediator: Mediator = container.resolve(Mediator)

        try:
            title, author, year = self.get_books_params()
        except ToMainMenuException:
            return

        book: Book
        book, *_ = mediator.handle_command(AddBookCommand(
            title=title.as_generic_type(),
            author=author.as_generic_type(),
            year=year.as_generic_type()
        ))

        print('Книга успешно добавлена!')
        print_book(book)

    def to_str_for_menu(self):
        return 'Добавить книгу'

    def get_books_params(self) -> tuple[Title, Author, Year]:
        while True:
            print('Введите название:')
            try:
                title = self._init_book_param(Title)
            except BookTitleTooShortException:
                print()
                print('Название книги слишком короткое. Попробуйте еще раз.')
                continue
            except BookTitleTooLongException:
                print()
                print('Название книги слишком длинное. Попробуйте еще раз.')
                continue
            except BookTitleIsEmptyException:
                print()
                print('Название книги не может быть пустым. Попробуйте еще раз.')
                continue

            print('Введите автора:')
            try:
                author = self._init_book_param(Author)
            except BookAuthorTooShortException:
                print()
                print('Автор слишком короткий. Попробуйте еще раз.')
                continue
            except BookAuthorTooLongException:
                print()
                print('Автор слишком длинный. Попробуйте еще раз.')
                continue
            except BookAuthorIsEmptyException:
                print()
                print('Автор не может быть пустым. Попробуйте еще раз.')
                continue

            print('Введите год издания:')
            try:
                year = self._init_book_param(Year)
            except BookYearIsEmptyException:
                print()
                print('Год издания не может быть пустым. Попробуйте еще раз.')
                continue
            except BookYearNotNumericException:
                print()
                print('Год издания должен быть числом. Попробуйте еще раз.')
                continue
            except BookYearMoreThanCurrentYearException:
                print()
                print('Год издания не может быть больше текущего. Попробуйте еще раз.')
                continue
            except BookYearMustBeFourDigitsException:
                print()
                print('Год издания должен содержать 4 цифры. Попробуйте еще раз.')
                continue

            return title, author, year

    def _init_book_param(self, param_type: Type[BT]) -> BaseValueObject:
        value = input()
        if value == 'x' or value == 'х':  # Русская и английская
            raise ToMainMenuException()

        return param_type(value)


class DeleteBookMenuItem(BaseMenuItem):

    def handle(self) -> None:
        container: Container = init_container()
        mediator: Mediator = container.resolve(Mediator)

        try:
            oid = self.get_book_params()
        except ToMainMenuException:
            return

        try:
            mediator.handle_command(DeleteBookCommand(oid))
        except BookNotFoundException:
            print(f'Книга с ID "{oid}" не найдена')

        print('Книга успешно удалена!')

    def to_str_for_menu(self):
        return 'Удалить книгу'

    def get_book_params(self) -> str:
        print('Введите ID книги:')
        return self._init_book_param()

    def _init_book_param(self) -> str:
        value = input()
        if value == 'x' or value == 'х':  # Русская и английская
            raise ToMainMenuException()

        return value


class FindBookMenuItem(BaseMenuItem):

    def handle(self) -> None:
        container: Container = init_container()
        mediator: Mediator = container.resolve(Mediator)

        try:
            title, author, year = self.get_books_params()
        except ToMainMenuException:
            return

        books: list[Book]
        books, *_ = mediator.handle_command(
            FindBookCommand(
                title=title,
                author=author,
                year=year
            )
        )

        if len(books) == 0:
            print('Книги не найдены')
            return

        print('Результаты поиска:')
        for book in books:
            print_book(book)

    def to_str_for_menu(self):
        return 'Найти книгу'

    def get_books_params(self) -> tuple[str, str, str]:
        print('Введите название (Чтобы не искать по этому фильтру введите пустое значение):')
        title = self._init_book_param()

        print('Введите автора (Чтобы не искать по этому фильтру введите пустое значение):')
        author = self._init_book_param()

        print('Введите год издания (Чтобы не искать по этому фильтру введите пустое значение):')
        year = self._init_book_param()

        return title, author, year

    def _init_book_param(self) -> str:
        value = input()
        if value == 'x' or value == 'х':  # Русская и английская
            raise ToMainMenuException()

        if value == '':
            value = None
        return value


class UpdateStatusMenuItem(BaseMenuItem):

    def handle(self) -> None:
        container: Container = init_container()
        mediator: Mediator = container.resolve(Mediator)

        try:
            oid = self.get_book_params()
        except ToMainMenuException:
            return

        try:
            mediator.handle_command(UpdateBookStatusCommand(oid))
        except BookNotFoundException(oid):
            print(f'Книга с ID "{oid}" не найдена')

        print('Статус книги успешно обновлен!')

    def to_str_for_menu(self):
        return 'Обновить статус книги'

    def get_book_params(self) -> str:
        print('Введите ID книги:')
        return self._init_book_param()

    def _init_book_param(self) -> str:
        value = input()
        if value == 'x' or value == 'х':  # Русская и английская
            raise ToMainMenuException()

        return value


class CloseProgramMenuItem(BaseMenuItem):

    def handle(self) -> None:
        exit()

    def to_str_for_menu(self):
        return 'Выход'
