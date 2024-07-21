from punq import Container
from pytest import fixture

from core.infra.repositories.base import BaseBooksRepository
from core.logic.container import _init_container
from core.logic.mediator import Mediator


@fixture(scope='function')
def container() -> Container:
    return _init_container(True)


@fixture()
def books_repository(container) -> BaseBooksRepository:
    return container.resolve(BaseBooksRepository)


@fixture()
def mediator(container) -> Mediator:
    return container.resolve(Mediator)
