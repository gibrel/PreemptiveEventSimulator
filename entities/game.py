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

    def get_by_id(self, obj_type: Type[T], uid: int) -> T | None:
        """
            Use example 'get_by_id(loc.City, 1100015)'.
        :param obj_type:
        :param uid:
        :return:
        """
        if obj_type not in self._CLASSES:
            return None
        try:
            return next((entity for entity in self._lists[obj_type] if entity.uid == uid), None)
        except:
            return None

    def insert(self, obj: T) -> bool:
        """

        :param obj:
        :return:
        """
        if type(obj) not in self._CLASSES:
            return False
        try:
            if self.get_by_id(type(obj), obj.uid) is None:
                self._lists[type(obj)].append(obj)
                return True
        except:
            return False

    def list(self, obj_type: Type[T]) -> list[T] | None:
        """

        :param obj_type: Type of the requested object.
        :return: List of all registered objects of given type.
        """
        if obj_type not in self._CLASSES:
            return None
        try:
            return self._lists[obj_type]
        except:
            return None

    def __str__(self) -> str:
        return (f'Total de:'
                f'\n\t{len(self._lists[loc.City])} municípios,'
                f'\n\t{len(self._lists[loc.MicroRegion])} microrregiões,'
                f'\n\t{len(self._lists[loc.ImmediateRegion])} regões imediatas,'
                f'\n\t{len(self._lists[loc.MediumRegion])} mesorregiões,'
                f'\n\t{len(self._lists[loc.IntermediateRegion])} regiões intermediárias,'
                f'\n\t{len(self._lists[loc.State])} unidades federativas,'
                f'\n\t{len(self._lists[loc.Region])} regiões e'
                f'\n\t{len(self._lists[loc.Country])} países'
                f'\nimportados!'
                f'\nTotal de:'
                f'\n\t{len(self._lists[spr.Player])} jogadores,'
                f'\n\t{len(self._lists[spr.Squad])} equipes e'
                f'\n\t{len(self._lists[spr.Team])} times'
                f'\ncriados!')

    def mass_import(self, cities: list(loc.City)) -> None:
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
            self.insert(city.micro_region.medium_region.state)
            self.insert(city.micro_region.medium_region.state.region)
            self.insert(city.micro_region.medium_region.state.region.country)
