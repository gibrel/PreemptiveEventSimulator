import enum


class Category:
    age_15_17 = "age_15_17"
    age_18_19 = "age_18_19"
    age_20_24 = "age_20_24"
    age_25_29 = "age_25_29"
    age_30_up = "age_30_up"


class Gender(enum.IntEnum):
    Female = enum.auto()
    Male = enum.auto()
    Unisex = enum.auto()
