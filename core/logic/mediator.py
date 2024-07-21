from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Type

from core.logic.commands.base import BaseCommandHandler, CT, CR, BaseCommand
from core.logic.exceptions.mediator import CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    """
    Класс Mediator для обработки и регистрации команд.

    Атрибуты:
    - command_map: Словарь, сопоставляющий типы команд со списком обработчиков команд.

    Методы:
    - register_command(self, command: Type[CT], command_handlers: Iterable[BaseCommandHandler[CT, CR]]) -> None:
        Регистрирует команду со своими соответствующими обработчиками команд.

    - handle_command(self, command: BaseCommand) -> Iterable[CR]:
        Обрабатывает команду, выполняя связанные с ней обработчики команд.
    """
    command_map: dict[Type[CT], list[BaseCommandHandler[CT, CR]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    def register_command(self, command: Type[CT], command_handlers: Iterable[BaseCommandHandler[CT, CR]]) -> None:
        """
        Регистрирует команду со своими соответствующими обработчиками команд.

        Аргументы:
        - command: Тип команды для регистрации.
        - command_handlers: Список обработчиков команд для команды.
        """
        self.command_map[command].extend(command_handlers)

    def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        """
        Обрабатывает команду, выполняя связанные с ней обработчики команд.

        Аргументы:
        - command: Команда для обработки.

        Возвращает:
        - Итерируемый объект результатов выполнения обработчиков команд.
        """
        command_type = command.__class__
        handlers = self.command_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [handler.handle(command) for handler in handlers]