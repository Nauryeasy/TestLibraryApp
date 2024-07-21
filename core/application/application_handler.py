from typing import Type

from core.application.menu_items.base import BaseMenuItem, get_menu_items


"""Класс для обработки запросов пользователя"""


class Handler:

    menu_items = list[BaseMenuItem]

    def __init__(self):
        self.menu_items = [menu_item() for menu_item in get_menu_items()]

    def start(self):
        while True:
            print()
            for index, item in enumerate(self.menu_items):
                print(f'{index} - {item.__str__()}')
            try:
                choice = int(input('Выберите пункт меню (Для возвращения в главное меню введите "x"): '))
            except ValueError:
                print()
                print('Пункт должен быть целым числом')
                continue
            try:
                self.menu_items[choice].handle()
            except IndexError:
                print()
                print('Такого пункта нет')
