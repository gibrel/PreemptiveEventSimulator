from abc import ABC


class Base(ABC):
    """
    Base class for entities in solution.
    """
    uid: int
    name: str

    def __init__(self, uid: int, name: str):
        self.uid, self.name = uid, name

    def __str__(self) -> str:
        pass


class Location(Base):
    """
    Base class for locations in solution.
    """

    def __init__(self, uid: int, name: str):
        super().__init__(uid, name)
