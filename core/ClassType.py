from enum import Enum


class ClassType(Enum):
    ADS1115ADCONVERTER = "Ads1115ADConverter", "ADC", ["address", "str"]
    INA219POWERSENSOR = "Ina219PowerSensor", "IPS", ["address", "str"]
    RELAY = "Relay", "REL", ["address", "str"], ["closed", "boolean"]
    M3HMOTORCONTROLLER = "M3HMotorcontroller", "M3H", ["address", "str"]
    TRACK = "Track", "TRA", ["length", "numeric"], ["radius", "integer"], ["slope","numeric"]
    TRACKGROUP = "TrackGroup", "TRG", ["track", "str"]
