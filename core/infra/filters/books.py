from dataclasses import dataclass


"""Фильтры для книг"""


@dataclass(frozen=True)
class BookFilters:
    title: str | None = None
    author: str | None = None
    year: str | None = None
    status: bool | None = None
