from enum import Enum


class ClassType(Enum):
    RASPERRYPIE = "RasperryPie", "RAS", ["name", "string"], ["master", "boolean"], ["database", "boolean"]
    ADS1115ADCONVERTER = "Ads1115ADConverter", "ADC", ["name", "string"], ["rasperrypie"], ["i2caddress", "string"]
    INA219POWERSENSOR = "Ina219PowerSensor", "IPS", ["name", "string"], ["rasperrypie"], ["i2caddress", "string"]
    RELAY = "Relay", "REL", ["name", "string"], ["rasperrypie"], ["gpio", "integer"], ["closed", "boolean"]
    M3HMOTORCONTROLLER = "M3HMotorcontroller", "M3H", ["name", "string"], ["rasperrypie"], ["i2caddress", "string"]
    MATRIX = "Matrix", "MAT", ["name", "string"], ["xlength", "integer"], ["ylength", "integer"], ["zlength", "integer"]
    PLANE = ("Plane", "PLA", ["name", "string"], ["matrix"], ["xlength", "integer"], ["ylength", "integer"], ["xpos", "integer"],
             ["ypos", "integer"], ["zpos", "integer"], ["xrot", "integer"], ["yrot", "integer"], ["zrot", "integer"])
    TRACK = ("Track", "TRA", ["name", "string"], ["plane"], ["xpos", "integer"], ["ypos", "integer"], ["rot", "integer"],
             ["zpos", "integer"], ["inclination", "numeric"], ["trackgroup"],
             ["blocked", "boolean"], ["rasperrypie"], ["m3hmotorcontroller"], ["motorcontrollerchannel", "integer"],
             ["ina219powersensor"], ["Relay"], ["analog", "boolean"], ["exact", "boolean"], ["dead", "boolean"],
             ["speedlimit", "numeric"])
    STRAIGHTTRACK = ("StraightTrack", "STR", ["name", "string"], ["length", "integer"],
                     ["xconnectiona", "integer"], ["yconnectiona", "integer"], ["zconnectiona", "integer"],
                     ["xconnectionb", "integer"], ["yconnectionb", "integer"], ["zconnectionb", "integer"],
                     ["track"], ["joinedtrackaoid", "string"], ["joinedtrackboid", "string"])
    TRACKGROUP = "TrackGroup", "TRG", ["name", "string"]