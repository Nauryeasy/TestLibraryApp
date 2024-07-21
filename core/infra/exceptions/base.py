from dataclasses import dataclass


@dataclass(eq=False)
class InfrastructureException(Exception):
    @property
    def message(self) -> str:
        return 'An error has occurred'

    def __str__(self) -> str:
        return self.message
