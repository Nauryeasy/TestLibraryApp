from functools import lru_cache

from punq import Container, Scope

from core.infra.repositories.base import BaseBooksRepository
from core.infra.repositories.books import MemoryJsonBooksRepository
from core.logic.commands.books import (
    AddBookCommandHandler,
    DeleteBookCommandHandler,
    FindBookCommandHandler,
    UpdateBookStatusCommandHandler,
    AddBookCommand,
    DeleteBookCommand,
    FindBookCommand,
    UpdateBookStatusCommand, GetBooksCommandHandler, GetBooksCommand
)
from core.logic.mediator import Mediator
from core.settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container(test_mode: bool = False) -> Container:
    """
        Инициализирует контейнер с необходимыми зависимостями и конфигурациями.

        Параметры:
            test_mode (bool, optional): Указывает, инициализируется ли контейнер в режиме тестирования. По умолчанию False.

        Возвращает:
            Container: Инициализированный контейнер с зарегистрированными зависимостями и конфигурациями.

        Описание:
            Эта функция инициализирует контейнер с необходимыми зависимостями и конфигурациями для приложения.
            Регистрируются следующие зависимости:
            - Config: Одиночный экземпляр класса Config.
            - AddBookCommandHandler: Обработчик для команды AddBookCommand.
            - DeleteBookCommandHandler: Обработчик для команды DeleteBookCommand.
            - FindBookCommandHandler: Обработчик для команды FindBookCommand.
            - UpdateBookStatusCommandHandler: Обработчик для команды UpdateBookStatusCommand.
            - GetBooksCommandHandler: Обработчик для команды GetBooksCommand.

            Также регистрируются две фабрики:
            - init_books_json_repository: Фабричная функция, которая инициализирует экземпляр MemoryJsonBooksRepository с
              соответствующим путем к базе данных в зависимости от режима тестирования.
            - init_mediator: Фабричная функция, которая инициализирует экземпляр Mediator и регистрирует необходимые обработчики команд.

            Затем контейнер возвращается для дальнейшего использования в приложении.
    """
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    container.register(AddBookCommandHandler)
    container.register(DeleteBookCommandHandler)
    container.register(FindBookCommandHandler)
    container.register(UpdateBookStatusCommandHandler)
    container.register(GetBooksCommandHandler)

    def init_books_json_repository() -> BaseBooksRepository:
        config: Config = container.resolve(Config)
        repo = MemoryJsonBooksRepository(config.json_database_path if not test_mode else config.test_database_path)

        return repo

    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_command(AddBookCommand, [container.resolve(AddBookCommandHandler)])
        mediator.register_command(DeleteBookCommand, [container.resolve(DeleteBookCommandHandler)])
        mediator.register_command(FindBookCommand, [container.resolve(FindBookCommandHandler)])
        mediator.register_command(UpdateBookStatusCommand, [container.resolve(UpdateBookStatusCommandHandler)])
        mediator.register_command(GetBooksCommand, [container.resolve(GetBooksCommandHandler)])

        return mediator

    container.register(BaseBooksRepository, factory=init_books_json_repository, scope=Scope.singleton)
    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
