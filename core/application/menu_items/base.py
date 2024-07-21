from abc import ABC, abstractmethod
from typing import Type


"""Абстрактный класс для элементов меню"""


class BaseMenuItem(ABC):

    @abstractmethod
    def handle(self) -> None:
        ...

    @abstractmethod
    def to_str_for_menu(self):
        ...

    def __str__(self):
        return self.to_str_for_menu()


from core.application.menu_items.app import AddBookMenuItem, GetBooksMenuItem


def get_menu_items() -> list[Type[BaseMenuItem]]:
    return BaseMenuItem.__subclasses__()
