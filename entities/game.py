from __future__ import annotations
from entities.base import Base
import entities.locations as loc
import entities.sports as spr
from typing import Type, TypeVar
from helpers.json_decoder import Decoder

T = TypeVar('T', bound=Base)


class Game:
    """
    This class is responsible to handle the game's data.
    """
    _CLASSES = {
        loc.Country, loc.Region, loc.State, loc.MediumRegion, loc.IntermediateRegion, loc.MicroRegion,
        loc.ImmediateRegion, loc.City, spr.Team, spr.Squad, spr.Player
    }
    _lists = {
        loc.Country: [], loc.Region: [], loc.State: [], loc.MediumRegion: [], loc.IntermediateRegion: [],
        loc.MicroRegion: [], loc.ImmediateRegion: [], loc.City: [], spr.Team: [], spr.Squad: [], spr.Player: []
    }

    def __init__(self):
        print('Starting to decode JSON files...')
        Decoder.decode()
        print('Decode of JSON files complete. Importing entities...')
        self.mass_import(Decoder.get_cities())
        print('Imported entities to system. Populating game...')

    def contains(self, obj_type: Type[T], filters=None) -> bool:
        """

        :param obj_type:
        :param filters:
        :return:
        """
        if obj_type not in self._CLASSES:
            return False
        try:
            if filters is None:
                return False
            return any(entity for entity in self._lists[obj_type] if filters(entity))
        except TypeError as e:
            print(f'[TypeError]: {e.args}')
            return False
        except KeyError as e:
            print(f'[KeyError]: {e.args}')
            return False
        except IndexError as e:
            print(f'[IndexError]: {e.args}')
            return False

    def check(self, obj_type: Type[T], uid: int | None = None, name: str | None = None) -> bool:
        """

        :param obj_type:
        :param uid:
        :param name:
        :return:
        """
        if obj_type not in self._CLASSES:
            return False
        try:
            if name is not None and uid is not None:
                return any((entity for entity in self._lists[obj_type] if entity.uid == uid and entity.name == name))
            elif uid is not None:
                return any((entity for entity in self._lists[obj_type] if entity.uid == uid))
            elif name is not None:
                return any((entity for entity in self._lists[obj_type] if entity.name == name))
            else:
                return False
        except TypeError as e:
            print(f'[TypeError]: {e.args}')
            return False
        except KeyError as e:
            print(f'[KeyError]: {e.args}')
            return False
        except IndexError as e:
            print(f'[IndexError]: {e.args}')
            return False

    def get_first(self, obj_type: Type[T], uid: int | None = None, name: str | None = None) -> T | None:
        """

        :param obj_type:
        :param uid:
        :param name:
        :return:
        """
        if obj_type not in self._CLASSES:
            return None
        try:
            if name is not None and uid is not None:
                return next((entity for entity in self._lists[obj_type] if entity.uid == uid and entity.name == name),
                            None)
            elif uid is not None:
                return next((entity for entity in self._lists[obj_type] if entity.uid == uid), None)
            elif name is not None:
                return next((entity for entity in self._lists[obj_type] if entity.name == name), None)
            else:
                return self._lists[obj_type][0]
        except TypeError as e:
            print(f'[TypeError]: {e.args}')
            return None
        except KeyError as e:
            print(f'[KeyError]: {e.args}')
            return None
        except IndexError as e:
            print(f'[IndexError]: {e.args}')
            return None

    def insert(self, obj: T, no_check: bool = False) -> bool:
        """

        :param obj:
        :param no_check:
        :return:
        """
        if type(obj) not in self._CLASSES:
            return False
        try:
            if no_check:
                self._lists[type(obj)].append(obj)
                return True
            # if not self.check(type(obj), obj.uid):
            if not self.contains(type(obj), lambda entity: entity.uid == obj.uid):
                self._lists[type(obj)].append(obj)
                return True
            else:
                return False
        except TypeError as e:
            print(f'[TypeError]: {e.args}')
            return False
        except KeyError as e:
            print(f'[KeyError]: {e.args}')
            return False
        except IndexError as e:
            print(f'[IndexError]: {e.args}')
            return False

    def lists(self, obj_type: Type[T], filters=None) -> list[T]:
        """

        :param obj_type:
        :param filters:
        :return:
        """
        if obj_type not in self._CLASSES:
            return []
        try:
            if filters is None:
                return self._lists[obj_type]
            else:
                return [entity for entity in self._lists[obj_type] if filters(entity)]
        except TypeError as e:
            print(f'[TypeError]: {e.args}')
            return []
        except KeyError as e:
            print(f'[KeyError]: {e.args}')
            return []
        except IndexError as e:
            print(f'[IndexError]: {e.args}')
            return []

    def count(self, obj_type: Type[T], filters=None) -> int:
        """

        :param obj_type:
        :param filters:
        :return:
        """
        if obj_type not in self._CLASSES:
            return 0
        try:
            if filters is None:
                return len(self._lists[obj_type])
            else:
                return len([entity for entity in self._lists[obj_type] if filters(entity)])
        except TypeError as e:
            print(f'[TypeError]: {e.args}')
            return 0
        except KeyError as e:
            print(f'[KeyError]: {e.args}')
            return 0
        except IndexError as e:
            print(f'[IndexError]: {e.args}')
            return 0

    def prints(self, obj_type: Type[T], filters=None) -> None:
        """

        :param obj_type:
        :param filters:
        :return:
        """
        if obj_type not in self._CLASSES:
            return
        for entity in self.lists(obj_type, filters):
            print(entity)

    def __str__(self) -> str:
        return (f'Total de:'
                f'\n\t{self.count(loc.City)} municípios,'
                f'\n\t{self.count(loc.MicroRegion)} microrregiões,'
                f'\n\t{self.count(loc.ImmediateRegion)} regões imediatas,'
                f'\n\t{self.count(loc.MediumRegion)} mesorregiões,'
                f'\n\t{self.count(loc.IntermediateRegion)} regiões intermediárias,'
                f'\n\t{self.count(loc.State)} unidades federativas,'
                f'\n\t{self.count(loc.Region)} regiões e'
                f'\n\t{self.count(loc.Country)} países'
                f'\nimportados!'
                f'\nTotal de:'
                f'\n\t{self.count(spr.Player)} jogadores,'
                f'\n\t{self.count(spr.Squad)} equipes e'
                f'\n\t{self.count(spr.Team)} times'
                f'\ncriados!')

    def mass_import(self, cities: list[loc.City]) -> None:
        """

        :param cities:
        :return:
        """
        for city in cities:
            self.insert(city)
            self.insert(city.micro_region)
            self.insert(city.immediate_region)
            self.insert(city.micro_region.medium_region)
            self.insert(city.immediate_region.intermediate_region)
            self.insert(city.state())
            self.insert(city.state().region)
            self.insert(city.state().region.country)
