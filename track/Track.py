import inspect
from typing import override
from database.Database import Database
from matrix.Plane import Plane
from pie_hardware.Ina219PowerSensor import Ina219PowerSensor
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadInitializationException, DBOrgaException
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller
from pie_hardware.RasperryPie import RasperryPie
from pie_hardware.Relay import Relay
from track.TrackGroup import TrackGroup


class Track(ClassBase):
    """
    The base object for a track
    """
    __TrackGroup : TrackGroup
    __blocked: bool
    __rasperry_pie: RasperryPie
    __motor_controller: M3HMotorcontroller
    __motor_controller_channel: int
    __ina_powersensor: Ina219PowerSensor
    __relay: Relay
    __plane: Plane
    __xpos: int
    __ypos: int
    __rot: int
    __zpos: int
    __inclination: float
    __analog: bool
    __exact: bool
    __dead: bool
    __speed_limit: float


    def __init__(self, name, plane:Plane, xpos:int, ypos:int, rot:int, zpos:int = None, inclination:float = None, track_group:TrackGroup = None, blocked:bool = False,
                 rasperry_pie:RasperryPie = None, motor_controller: M3HMotorcontroller = None, motor_controller_channel:int= None, ina_powersensor:Ina219PowerSensor = None,
                 relay:Relay = None, analog:bool = False, exact:bool = False, dead:bool = False, speed_limit:float = 9.9, oid:str = None):
        """
        Initialize track section with its controller parts, do not use manually
        """
        caller_stack = inspect.stack()
        legal_db_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_db_call = True
            if not legal_db_call:
                raise BadInitializationException(
                    "There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.TRACK, name, oid)
        else:
            super().__init__(ClassType.TRACK, name)

        self.__track_group = track_group
        self.__blocked = blocked
        self.__rasperry_pie = rasperry_pie
        self.__motor_controller = motor_controller
        self.__motor_controller_channel = motor_controller_channel
        self.__ina_powersensor = ina_powersensor
        self.__relay = relay
        self.__plane = plane
        self.__xpos = xpos
        self.__ypos = ypos
        self.__rot = rot
        self.__inclination = inclination
        self.__zpos = zpos
        self.__analog = analog
        self.__exact = exact
        self.__dead = dead
        self.__speed_limit = speed_limit

        if not legal_db_call:
            self.__db_write_to_db__()
    """
    END create functions
    """



    """
    START db functions
    """
    @classmethod
    def __db_build_class__(cls, data:list):
        """
        puts the given parameter in this Track object, only to be used by the database to load an already existing track
        from the database, to create a new track, use the constructor directly and NEVER set the parameter "oid"
        :return: the Track object with the given parameter
        """
        new_track = object.__new__(cls)
        new_track.__init__(data[1], data[2], data[3], data[4], data[5], data[6],data[7], data[8], data[9], data[10],
                           data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[0])
        return new_track


    @override
    def __db_write_to_db__(self):
        sql_string_1 = "INSERT INTO track (oid, name, plane, xpos, ypos, rot, zpos, inclination, "
        sql_string_2 = (" VALUES ('" + self.get_oid() + "', '" + self.__plane.get_oid() + "', '" + self.get_name() +
                        "', '" + str(self.__xpos) + "', '" + str(self.__ypos) + "', '" + str(self.__rot) + "', '" +
                        str(self.__zpos) + "', '" + str(self.__inclination) + "', '")
        
        if self.__track_group is not None:
            sql_string_1 = sql_string_1 + "trackgroup, "
            sql_string_2 = sql_string_2 +  self.__track_group.get_oid() + "', '"
        
        sql_string_1 = sql_string_1 + "blocked, "
        sql_string_2 = sql_string_2 + str(self.__blocked) + "', '"

        if self.__rasperry_pie is not None:
            sql_string_1 = sql_string_1 + "rasperrypie, "
            sql_string_2 = sql_string_2 + self.__rasperry_pie.get_oid() + "', '"

        if self.__motor_controller is not None:
            sql_string_1 = sql_string_1 + "m3hmotorcontroller, motorcontrollerchannel, "
            sql_string_2 = sql_string_2 + self.__motor_controller.get_oid() + "', " + str(self.__motor_controller_channel) + ", '"

        if self.__ina_powersensor is not None:
            sql_string_1 = sql_string_1 + "ina219powersensor, "
            sql_string_2 = sql_string_2 + self.__ina_powersensor.get_oid()  + "', '"

        if self.__relay is not None:
            sql_string_1 = sql_string_1 + "relay, "
            sql_string_2 = sql_string_2 + self.__relay.get_oid() + "', '"

        sql_string_1 = sql_string_1 + "analog, exact, dead, speedlimit)"
        sql_string_2 = (sql_string_2 + str(self.__analog) + "', '" + str(self.__exact) + "', '" + str(self.__dead) +
                        "', '" + str(self.__speed_limit) + "')")

        Database.run_sql_query(sql_string_1 + sql_string_2, False)
    """
    END db functions
    """




    """
    START public general functions
    """
    @classmethod
    def create_new(cls, name, plane:Plane, xpos:int, ypos:int, rot:int, zpos:int, inclination:int = 0, track_group:TrackGroup = None, blocked:bool = False,
                   rasperry_pie:RasperryPie = None, motor_controller: M3HMotorcontroller = None, motor_controller_channel:int = None, ina_powersensor:Ina219PowerSensor = None,
                   relay:Relay = None, analog:bool = False, exact:bool = False, dead:bool = False, speed_limit:float = 9.9):
        """
            Do not call this directly, it is called by the
        """

        if xpos < 0 or ypos < 0 or rot < 0:
            raise BadInitializationException("There was an attempt to create a track with a negative position or rotation:\n"
                                             "xpos: " + str(xpos) + "\n"
                                             "ypos: " + str(ypos) + "\n"
                                             "xrot: " + str(rot) + "\n")

        if rot >= 360:
            raise BadInitializationException("There was an attempt to create a track with a rotation of 360° or higher:\n"
                                             "xrot: " + str(rot) +"\n")

        if inclination is None:
            inclination = 0

        if -90 > inclination > 90:
            raise BadInitializationException("There was an attempt to create a track with a inclination over 90° or under -90°")

        if (motor_controller is not None and motor_controller_channel is None) or (motor_controller is None and motor_controller_channel is not None):
            raise BadInitializationException("There was an attempt to initialize a track with only a motor controller or "
                                             "a motor controller channel, they have ether both to be set or none")

        if motor_controller is not None and motor_controller_channel:
            names_of_found_controller = Database.run_sql_query("SELECT name FROM track WHERE m3hmotorcontroller = '" +
                                                               motor_controller.get_oid() + "' AND motorcontrollerchannel = " +
                                                               str(motor_controller_channel))
            if names_of_found_controller is not None:
                if isinstance(names_of_found_controller, str):
                    raise BadInitializationException("There was  an attempt to create a track on a motor controller channel that is already in use\n"
                                                     "motor_controller: '" + motor_controller.get_name() + "'\n"
                                                     "channel: " + str(motor_controller_channel))
                else:
                    raise DBOrgaException("There are more than 1 entries in the database for a motor controller\n"
                                                     "motor_controller: '" + motor_controller.get_name() + "'\n"
                                                     "channel: " + str(motor_controller_channel))

        if ina_powersensor is not None:
            names_of_found_powersensor = Database.run_sql_query("SELECT name FROM track WHERE ina219powersensor = '" +
                                                               ina_powersensor.get_oid() + "'")
            if names_of_found_powersensor is not None:
                if isinstance(names_of_found_powersensor, str):
                    raise BadInitializationException("here was an attempt to create a track with a powersensor that is already in use\n"
                                                     "powersensor: " + ina_powersensor.get_name())
                else:
                    raise DBOrgaException("There are more than 1 entries in the database for a powersensor\n"
                                                     "powersensor: " + ina_powersensor.get_name())

        if relay is not None:
            names_of_found_relay = Database.run_sql_query("SELECT name FROM track WHERE relay = '" + relay.get_oid() + "'")
            if names_of_found_relay is not None:
                if isinstance(names_of_found_relay, str):
                    raise BadInitializationException("here was an attempt to create a track with a relay that is already in use\n"
                                                     "relay: " + relay.get_name())
                else:
                    raise DBOrgaException("There are more than 1 entries in the database for a relay\n"
                                                     "relay: " + relay.get_name())

        if speed_limit != 9.9 and 0 > speed_limit > 5:
            raise BadInitializationException("There was an attempt to create a track with a speed limit"
                                             "above 5 m/s, this is not allowed \n The track top speed is not scaled"
                                             "down but based the actual speed that the model train is running, 5m/s"
                                             "are 18km/h and scaled to 1:87, 1566km/h\n If the track should not have"
                                             "a speed limitation of the value is 9.9, which is also the default value")

        if rasperry_pie is None and (motor_controller is not None or ina_powersensor is not None or relay is not None):
            raise BadInitializationException("There was an attempt to create a track with no rasperry pie but"
                                             "at least one of of motor controller, powersensor or relay not None")

        if motor_controller is not None and rasperry_pie is not motor_controller.get_rasperry_pie():
            raise BadInitializationException("There was an attempt to create a track with the motor controller "
                                             + motor_controller.get_name() + " that is on another rasperry pie than itself:\n"
                                             "Tracks rasperry pie:  " + rasperry_pie.get_name() + "\n"
                                             "motor controllers pie:" + motor_controller.get_rasperry_pie().get_name())

        if ina_powersensor is not None and rasperry_pie is not ina_powersensor.get_rasperry_pie():
            raise BadInitializationException("There was an attempt to create a track with the power sensor,"
                                             +ina_powersensor.get_name() + " that is on another rasperry pie than itself:\n"
                                             "Tracks rasperry pie:  " + rasperry_pie.get_name() + "\n"
                                             "power sensors pie:" + ina_powersensor.get_rasperry_pie().get_name())

        if relay is not None and rasperry_pie is not relay.get_rasperry_pie():
            raise BadInitializationException("There was an attempt to create a track with the relay," +
                                             relay.get_name() + " that is on another rasperry pie than itself:\n"
                                             "Tracks rasperry pie:  " + rasperry_pie.get_name() + "\n"
                                             "motor controllers pie:" + relay.get_rasperry_pie().get_name())

        new_track = object.__new__(cls)
        new_track.__init__(name, plane,xpos, ypos, rot, zpos, inclination, track_group, blocked, rasperry_pie,
                           motor_controller, motor_controller_channel, ina_powersensor, relay, analog, exact, dead, speed_limit)
        return new_track


    @override
    def save(self):
        """
        Saves the current state of this track into the database
        """
        print("Noch nicht implementiert Track.save")


    def shutdown(self):
        """
        Cleans the track object up
        :return: nothing
        """
        self.__db_write_to_db__()
    """
    END public general functions
    """







    def copy(self):
        pass