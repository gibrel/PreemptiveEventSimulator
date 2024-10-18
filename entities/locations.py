from __future__ import annotations
from entities.base import Location
from helpers.enums import Category


class Country(Location):
    """
    Country entity class.
    """

    abbreviation: str

    def __init__(self, uid: int, name: str, abbreviation: str):
        super().__init__(uid, name)
        self.abbreviation = abbreviation

    def __str__(self) -> str:
        return f"{self.uid}\t|\t{self.name}\t|\t{self.abbreviation}"


class Region(Location):
    """
    Region entity class.
    """

    abbreviation: str
    country: Country

    def __init__(self, uid: int, name: str, abbreviation: str, country: Country):
        super().__init__(uid, name)
        self.abbreviation, self.country = abbreviation, country

    def __str__(self) -> str:
        return f"{self.uid}\t|\t{self.name}"


class State(Location):
    """
    State entity class.
    """

    abbreviation: str
    region: Region

    def __init__(self, uid: int, name: str, abbreviation: str, region: Region):
        super().__init__(uid, name)
        self.abbreviation, self.region = abbreviation, region

    def __str__(self) -> str:
        return (
            f"{self.uid}\t|\t{self.name}\t|\t{self.abbreviation}\t|\t{self.region.name}"
        )

    def country(self) -> Country:
        return self.region.country


class MediumRegion(Location):
    """
    Medium region entity class.
    """

    state: State

    def __init__(self, uid: int, name: str, state: State):
        super().__init__(uid, name)
        self.state = state

    def __str__(self) -> str:
        return f"{self.uid}\t|\t{self.name}\t|\t{self.state.name}"

    def region(self) -> Region:
        return self.state.region

    def country(self) -> Country:
        return self.state.region.country


class IntermediateRegion(Location):
    """
    Intermediate region entity class.
    """

    state: State

    def __init__(self, uid: int, name: str, state: State):
        super().__init__(uid, name)
        self.state = state

    def __str__(self) -> str:
        return f"{self.uid}\t|\t{self.name}\t|\t{self.state.name}"

    def region(self) -> Region:
        return self.state.region

    def country(self) -> Country:
        return self.state.region.country


class MicroRegion(Location):
    """
    Micro region entity class.
    """

    medium_region: MediumRegion

    def __init__(self, uid: int, name: str, medium_region: MediumRegion):
        super().__init__(uid, name)
        self.medium_region = medium_region

    def __str__(self) -> str:
        return f"{self.uid}\t|\t{self.name}\t|\t{self.medium_region.name} - {self.state().abbreviation}"

    def state(self) -> State:
        return self.medium_region.state

    def region(self) -> Region:
        return self.medium_region.state.region

    def country(self) -> Country:
        return self.medium_region.state.region.country


class ImmediateRegion(Location):
    """
    Immediate region entity class.
    """

    intermediate_region: IntermediateRegion

    def __init__(self, uid: int, name: str, intermediate_region: IntermediateRegion):
        super().__init__(uid, name)
        self.intermediate_region = intermediate_region

    def __str__(self) -> str:
        return (
            f"{self.uid}\t|\t{self.name}\t|\t{self.intermediate_region.name}"
            f" - {self.state().abbreviation}"
        )

    def state(self) -> State:
        return self.intermediate_region.state

    def region(self) -> Region:
        return self.intermediate_region.state.region

    def country(self) -> Country:
        return self.intermediate_region.state.region.country


class City(Location):
    """
    City entity class.
    """

    inhabitants: dict
    max_teams: dict
    immediate_region: ImmediateRegion
    micro_region: MicroRegion

    def __init__(
        self,
        uid: int,
        name: str,
        immediate_region: ImmediateRegion,
        micro_region: MicroRegion,
    ):
        super().__init__(uid, name)
        self.immediate_region, self.micro_region = immediate_region, micro_region
        self.inhabitants = {
            Category.age_15_17: 0,
            Category.age_18_19: 0,
            Category.age_20_24: 0,
            Category.age_25_29: 0,
            Category.age_30_up: 0,
        }
        self.max_teams = {
            Category.age_15_17: 0,
            Category.age_18_19: 0,
            Category.age_20_24: 0,
            Category.age_25_29: 0,
            Category.age_30_up: 0,
        }

    def __str__(self) -> str:
        return f"{self.uid}\t|\t{self.name}\t|\t{self.state().abbreviation}"

    def full_print(self) -> str:
        return (
            f"\n\t{self.name} - {self.state().abbreviation}\n\n"
            + f"\t\tEstado:\t{self.state().name} - {self.state().abbreviation}\n"
            + f"\t\tRegião Intermediária:\t{self.intermediate_region().name}\t\tRegião Imediata:\t{self.immediate_region.name}\n"
            + f"\t\tMeso Região:\t{self.medium_region().name}\t\tMicro Região:\t{self.micro_region.name}\n\n"
            + "\t\tPopulação:\n"
            + f"\t\t\tDe  15 a 17:\t{self.inhabitants[Category.age_15_17]}\t\t\tDe  18 a 19:\t{self.inhabitants[Category.age_18_19]}\t\t\tDe  20 a 24:\t{self.inhabitants[Category.age_20_24]}\n"
            + f"\t\t\tDe  25 a 29:\t{self.inhabitants[Category.age_25_29]}\t\t\tAcima de 30:\t{self.inhabitants[Category.age_30_up]}\n\n"
        )

    def intermediate_region(self) -> IntermediateRegion:
        return self.immediate_region.intermediate_region

    def medium_region(self) -> MediumRegion:
        return self.micro_region.medium_region

    def state(self) -> State:
        return self.micro_region.medium_region.state

    def region(self) -> Region:
        return self.micro_region.medium_region.state.region

    def country(self) -> Country:
        return self.micro_region.medium_region.state.region.country
