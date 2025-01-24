from enum import Enum


class ClassType(Enum):
    RASPERRYPIE = "RasperryPie", "RAS", ["name", "string"], ["master", "boolean"], ["database", "boolean"]
    ADS1115ADCONVERTER = "Ads1115ADConverter", "ADC", ["rasperrypie"], ["name", "string"], ["i2caddress", "string"]
    INA219POWERSENSOR = "Ina219PowerSensor", "IPS", ["name", "string"], ["rasperrypie"], ["i2caddress", "string"]
    RELAY = "Relay", "REL", ["name", "string"], ["rasperrypie"], ["gpio", "integer"], ["closed", "boolean"]
    M3HMOTORCONTROLLER = "M3HMotorcontroller", "M3H", ["name", "string"], ["rasperrypie"], ["i2caddress", "string"]
    TRACK = "Track", "TRA", ["name", "string"], ["trackgroup"], ["rasperrypie"], ["neighbour1", "string"], ["neighbour2", "string"], ["blocked", "boolean"], ["length", "numeric"], ["radius", "integer"], ["slope", "numeric"], ["ina219powersensor"], ["Relay"], ["m3hmotorcontroller"], ["dead", "boolean"]
    TRACKGROUP = "TrackGroup", "TRG", ["name", "string"]