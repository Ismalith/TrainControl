from enum import Enum


class ClassType(Enum):
    ADS1115ADCONVERTER = "ADC", ["address", "str"]
    INA219AMPSENS = "IAS", ["address", "str"]
    RELAY = "REL", ["address", "str"]
    M3HMOTORCONTROLLER = "M3H", ["address", "str"]
    TRACK = "TRA", ["length", "numeric"], ["radius", "integer"], ["slope","numeric"]
    TRACKGROUP = "TRG", ["track", "str"]
