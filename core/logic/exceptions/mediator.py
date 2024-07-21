from dataclasses import dataclass

from core.logic.exceptions.base import LogicException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f'Command handlers for "{self.command_type}" are not registered'
