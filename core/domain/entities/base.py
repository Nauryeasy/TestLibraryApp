import uuid
from dataclasses import dataclass, field


"""Абстрактный класс представляющий сущности предметной области"""


@dataclass
class BaseEntity:
    oid: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        kw_only=True
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: 'BaseEntity') -> bool:
        return self.oid == other.oid
