from dataclasses import dataclass, field

from core.domain.entities.base import BaseEntity
from core.domain.values.books import Title, Author, Year, Status


"""Базовое представление сущности книг. Получилась DTO`шка, так как не хотел добавлять сюда лишний функционал,
Чтобы энтити не знали о существовании других слоев, а не связанного с ними функционала не нашлось
"""


@dataclass
class Book(BaseEntity):
    title: Title
    author: Author
    year: Year
    status: Status = field(default=Status(True))  # True - В наличии, False - Выдана
