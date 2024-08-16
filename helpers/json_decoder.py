from __future__ import annotations
import json
import math
import entities.locations as loc
from helpers.enums import Category


class Decoder:
    """
    Class responsible to decode the JSON files containing location data.
    """
    _cities: list[loc.City] = []
    LOCATION_DATA = "data/municipios.json"
    INHABITANTS_DATA = "data/distribuicao.json"
    PERCENT_OF_ATHLETES = 0.07
    ATHLETES_IN_SQUAD = 22

    @classmethod
    def decode(cls):
        cls.decode_locations()
        cls.decode_inhabitants()

    @classmethod
    def decode_inhabitants(cls) -> None:
        with open(cls.INHABITANTS_DATA, encoding="utf8") as inhabitants_json:
            inhabitants_data = json.load(inhabitants_json)
            for city_data in inhabitants_data:
                cls.import_inhabitants(city_data)

    @classmethod
    def import_inhabitants(cls, obj: dict) -> None:
        props = ["uid", "age_15_17", "age_18_19", "age_20_24", "age_25_29", "age_30_up"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            ct = next((entity for entity in cls._cities if (entity.uid == obj["uid"])), None)
            if ct is not None:
                ct.inhabitants[Category.age_15_17] = obj[Category.age_15_17]
                ct.inhabitants[Category.age_18_19] = obj[Category.age_18_19]
                ct.inhabitants[Category.age_20_24] = obj[Category.age_20_24]
                ct.inhabitants[Category.age_25_29] = obj[Category.age_25_29]
                ct.inhabitants[Category.age_30_up] = obj[Category.age_30_up]
                ct.max_teams[Category.age_15_17] = cls.calculate_teams(ct.inhabitants[Category.age_15_17])
                ct.max_teams[Category.age_18_19] = cls.calculate_teams(ct.inhabitants[Category.age_18_19])
                ct.max_teams[Category.age_20_24] = cls.calculate_teams(ct.inhabitants[Category.age_20_24])
                ct.max_teams[Category.age_25_29] = cls.calculate_teams(ct.inhabitants[Category.age_25_29])
                ct.max_teams[Category.age_30_up] = cls.calculate_teams(ct.inhabitants[Category.age_30_up])

    @classmethod
    def get_cities(cls) -> list[loc.City]:
        return cls._cities

    @classmethod
    def decode_locations(cls) -> None:
        with open(cls.LOCATION_DATA, encoding="utf8") as cities_json:
            cities_data = json.load(cities_json)
            for city_data in cities_data:
                cls._cities.append(cls.city_decoder(city_data))

    @classmethod
    def city_decoder(cls, obj: dict) -> loc.City | None:
        props = ["uid", "name", "micro_region", "immediate_region"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.City(obj['uid'], obj['name'], cls.immediate_region_decoder(obj['immediate_region']),
                            cls.micro_region_decoder(obj['micro_region']))
        return None

    @classmethod
    def immediate_region_decoder(cls, obj: dict) -> loc.ImmediateRegion | None:
        props = ["uid", "name", "intermediate_region"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.ImmediateRegion(obj['uid'], obj['name'],
                                       cls.intermediate_region_decoder(obj['intermediate_region']))
        return None

    @classmethod
    def intermediate_region_decoder(cls, obj: dict) -> loc.IntermediateRegion | None:
        props = ["uid", "name", "state"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.IntermediateRegion(obj['uid'], obj['name'], cls.state_decoder(obj['state']))
        return None

    @classmethod
    def micro_region_decoder(cls, obj: dict) -> loc.MicroRegion | None:
        props = ["uid", "name", "medium_region"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.MicroRegion(obj['uid'], obj['name'], cls.medium_region_decoder(obj["medium_region"]))
        return None

    @classmethod
    def medium_region_decoder(cls, obj: dict) -> loc.MediumRegion | None:
        props = ["uid", "name", "state"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.MediumRegion(obj['uid'], obj['name'], cls.state_decoder(obj['state']))
        return None

    @classmethod
    def state_decoder(cls, obj: dict) -> loc.State | None:
        props = ["uid", "name", "region"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.State(obj['uid'], obj['name'], obj['abbreviation'], cls.region_decoder(obj['region']))
        return None

    @classmethod
    def region_decoder(cls, obj: dict) -> loc.Region | None:
        props = ["uid", "name", "abbreviation", "country"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.Region(obj['uid'], obj['name'], obj['abbreviation'], cls.country_decoder(obj['country']))
        return None

    @classmethod
    def country_decoder(cls, obj: dict) -> loc.Country | None:
        props = ["uid", "name", "abbreviation"]
        if all(prop in obj for prop in props) and type(obj) is dict:
            return loc.Country(obj['uid'], obj['name'], obj['abbreviation'])
        return None

    @classmethod
    def calculate_teams(cls, population: int) -> int:
        computed_teams = math.sqrt(population * cls.PERCENT_OF_ATHLETES / cls.ATHLETES_IN_SQUAD)
        return math.ceil(computed_teams) if population > 0 else 0
