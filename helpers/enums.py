import enum


class Position:
    GK = 'Goalkeeper'
    DL = 'Defender Left'
    DR = 'Defender Right'
    DC = 'Defender Center'
    DML = 'Defensive Midfielder Left'
    DMR = 'Defensive Midfielder Right'
    DMC = 'Defensive Midfielder Center'
    ML = 'Midfielder Left'
    MR = 'Midfielder Right'
    MC = 'Midfielder Center'
    AML = 'Attacking Midfielder Left'
    AMR = 'Attacking Midfielder Right'
    AMC = 'Attacking Midfielder Center'
    FL = 'Foward Left'
    FR = 'Foward Right'
    FC = 'Foward Center'
    SW = 'Sweeper'
    LWB = 'Left Wingback'
    RWB = 'Right Wingback'
    RB = 'Right Back'
    LB = 'Left Back'
    CB = 'Center Back'
    LW = 'Left Wing'
    RW = 'Right Wing'


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
