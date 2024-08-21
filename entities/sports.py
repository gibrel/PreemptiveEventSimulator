from __future__ import annotations
from entities.base import Base
from helpers.enums import Category
from entities.locations import City


class Team(Base):
    """
    Team entity class.
    """
    city: City

    def __init__(self, uid: int, name: str, city: City):
        super().__init__(uid, name)
        self.city = city

    def __str__(self) -> str:
        return (f'{self.uid}\t|\t{self.name}\t|'
                f'\t{self.city.name} - {self.city.state().abbreviation}')


class Squad(Base):
    """
    Squad entity class.
    """
    category: Category
    team: Team

    def __init__(self, uid: int, name: str, category: Category, team: Team):
        super().__init__(uid, name)
        self.category, self.team = category, team

    def __str__(self) -> str:
        return f'{self.uid}\t|\t{self.name}\t|\t{self.team.name}'


class Player(Base):
    """
    Player entity class.
    """
    surname: str
    age: int
    skill: int
    squad: Squad | None

    def __init__(self, uid: int, name: str, surname: str, age: int, skill: int, squad: Squad | None = None):
        super().__init__(uid, name)
        self.surname, self.age, self.skill, self.squad = surname, age, skill, squad

    def __str__(self) -> str:
        if self.squad is None:
            return f'{self.uid}\t|\t{self.name} {self.surname}\t|\t{self.age}\t|\t{self.skill}'
        else:
            return (f'{self.uid}\t|\t{self.name} {self.surname}\t|\t{self.age}\t|\t{self.skill}\t|'
                    f'\t{self.squad.name}\t|\t{self.squad.team.name}')
