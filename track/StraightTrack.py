import inspect
from typing import override

from core.ClassBase import ClassBase
from database.Database import Database
from matrix.Calculations import Calculations
from matrix.Plane import Plane
from pie_hardware.Ina219PowerSensor import Ina219PowerSensor
from track.Track import Track
from core.ClassType import ClassType
from core.Exceptions import BadInitializationException
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller
from pie_hardware.RasperryPie import RasperryPie
from pie_hardware.Relay import Relay
from track.TrackGroup import TrackGroup


class StraightTrack(ClassBase):
    """
    The base object for a track
    """
    __length: int
    __x_connection_a: int
    __y_connection_a: int
    __z_connection_a: int
    __joined_track_a_oid: str
    __x_connection_b: int
    __y_connection_b: int
    __z_connection_b: int
    __joined_track_b_oid: str
    __track: Track



    def __init__(self, name: str, length: int, x_connection_a:int, y_connection_a:int, z_connection_a:int, x_connection_b:int, y_connection_b:int, z_connection_b:int, track:Track, joined_track_a_oid:str = None, joined_track_b_oid:str = None, oid:str = None):
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
            super().__init__(ClassType.STRAIGHTTRACK, name, oid)
        else:
            super().__init__(ClassType.STRAIGHTTRACK, name)

        self.__length = length
        self.__x_connection_a = x_connection_a
        self.__y_connection_a = y_connection_a
        self.__z_connection_a = z_connection_a
        self.__x_connection_b = x_connection_b
        self.__y_connection_b = y_connection_b
        self.__z_connection_b = z_connection_b
        self.__joined_track_a_oid = joined_track_a_oid
        self.__joined_track_b_oid = joined_track_b_oid
        self.__track = track
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
        print(data[1], data[2], data[3], data[4], data[5], data[6],data[7], data[8], data[9], data[10], data[11], data[0])
        new_track.__init__(data[1], data[2], data[3], data[4], data[5], data[6],data[7], data[8], data[9], data[10], data[11], data[0])
        return new_track

    @override
    def __db_write_to_db__(self):
        sql_string_1 = "INSERT INTO public.straighttrack (oid, name, length, xconnectiona, yconnectiona, zconnectiona, xconnectionb, yconnectionb, zconnectionb, track"
        sql_string_2 = (" VALUES ('" + self.get_oid() + "', '" + self.get_name() + "', '" + str(self.__length) + "', '"
                        + str(self.__x_connection_a) + "', '" + str(self.__y_connection_a) + "', '" + str(self.__z_connection_a) + "', '"
                        + str(self.__x_connection_b) + "', '" + str(self.__y_connection_b) + "', '" + str(self.__z_connection_b) + "', '"
                        + self.__track.get_oid())

        if self.__joined_track_a_oid is not None:
            sql_string_1 = sql_string_1 + ", joinedtrackaoid"
            sql_string_2 = sql_string_2 + ", " + self.__joined_track_a_oid

        if self.__joined_track_b_oid is not None:
            sql_string_1 = sql_string_1 + ", joinedtrackboid"
            sql_string_2 = sql_string_2 + ", " + self.__joined_track_b_oid

        sql_string_1 = sql_string_1 + ")"
        sql_string_2 = sql_string_2 + "')"
        sql_insert = sql_string_1 + sql_string_2
        Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, plane:Plane, name = None, xpos:int = None, ypos:int = None, zpos:int = 0, length: int = 0, rot:int = 0, inclination:float = 0, x_connection_a:int = None,
                   y_connection_a:int = None, z_connection_a:int = 0, x_connection_b:int = None, y_connection_b:int = None, z_connection_b:int = 0,
                   joined_track_a:Track = None, joined_track_b:Track = None, track_group:TrackGroup = None,
                   rasperry_pie:RasperryPie = None, motor_controller: M3HMotorcontroller = None, motor_controller_channel:int = None, ina_powersensor:Ina219PowerSensor = None,
                   relay:Relay = None, analog:bool = False, exact:bool = False, dead:bool = False, blocked:bool = False, speed_limit:float = 9.9):
        """
        Creation methode to create and write a new straight track to the database, only create new straight track with this method
        :param name:
        :param track_group: to group the new track with other track elements together
        :param blocked: true if a RollingStock Object is currently on this track
        :param plane: the plane this track is laying on
        :param xpos: the x position of the middle point this track on the plane
        :param ypos: the y position of the middle point this track on the plane
        :param rot: the rotation around the middle point of this track flat on the plane
        :param zpos: the z position of the middle point this track on the plane, default is 0
        :param inclination: the inclination of this this track on the plane, default is 0 degrees
        :param rasperry_pie: the rasperry pie this track and its pie hardware components belong to
        :param motor_controller: the motor controller that is powering this track
        :param motor_controller_channel: the channel of the motor controller that is used for this track
        :param ina_powersensor: the power sensor that detects if a powered object is on this track and how much power is using
        :param relay: the relay that switches between digital and analog mode for this track
        :param analog: set true if this track is currently in analog mode
        :param exact: set true if this track has it's length values exactly measured and can be used to recalculate the speed and power relation of a train
        :param dead: set true if this track is not powered
        :param speed_limit: the maximal speed in real m/s that is allowed on this track the max allowed speedlimit is 5m/s, per default is deactivated with 9.9m/s
        :param length: the length of the new track
        :param x_connection_a: the x coordination of the first connection of this track to another track
        :param y_connection_a: the y coordination of the first connection of this track to another track
        :param z_connection_a: the z coordination of the first connection of this track to another track
        :param x_connection_b: the x coordination of the second connection of this track to another track
        :param y_connection_b: the y coordination of the second connection of this track to another track
        :param z_connection_b: the z coordination of the second connection of this track to another track
        :param joined_track_a: A connected Track on side a
        :param joined_track_b: A connected Track on side a
        :return: the newly created power track
        """
        if name is None:
            highest_generic_name = Database.run_sql_query("SELECT name FROM straighttrack WHERE name ~ '^StraightTrack \\d+$' ORDER BY name DESC LIMIT 1")
            if highest_generic_name is not None:
                name = "StraightTrack " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
            else:
                name = "StraightTrack 1"
        else:
            found_power_sensors_with_same_name = int(Database.run_sql_query("SELECT count(oid) FROM straighttrack "
                "WHERE name = '" + name + "'"))
            if found_power_sensors_with_same_name > 0:
                raise BadInitializationException("A track with the name " + name + " is already in use" )

        if length < 0:
            raise BadInitializationException("There was ann attempt to create straighttrack " + name + " with a negative length " + str(length))

        pos_active = False
        if xpos and ypos is not None:
            pos_active = True
        elif xpos or ypos is not None or zpos != 0:
            raise BadInitializationException("There was an attempt to initialize the track " + name + " with x, y or z coordinates but not all where set" +
                                             "x: " + str(xpos) + "\n" +
                                             "y: " + str(ypos) + "\n" +
                                             "z: " + str(zpos))

        rot_active = False
        if rot != 0:
            rot_active = True

        connection_a_active = False
        if x_connection_a and y_connection_a is not None:
            connection_a_active = True
        elif x_connection_a or y_connection_a is not None or z_connection_a != 0:
            raise BadInitializationException("There was an attempt to initialize the track " + name + " with first connection coordinates but not all where set" +
                                             "x: " + str(x_connection_a) + "\n" +
                                             "y: " + str(y_connection_a) + "\n" +
                                             "z: " + str(z_connection_a))

        connection_b_active = False
        if x_connection_b and y_connection_b is not None:
            connection_b_active = True
        elif x_connection_b or y_connection_b is not None or z_connection_b != 0:
            raise BadInitializationException("There was an attempt to initialize the track " + name + " with second connection coordinates but not all where set" +
                                             "x: " + str(x_connection_b) + "\n" +
                                             "y: " + str(y_connection_b) + "\n" +
                                             "z: " + str(z_connection_b))

        if connection_a_active and (not plane.are_coordinates_legal(x_connection_a, y_connection_a, z_connection_a)):
            raise BadInitializationException("There was an attempt to set connection coordinates that are outside the matrix for track " +
                                             name + " Coordinates:\n" +
                                             "x: " + str(x_connection_a) + "\n" +
                                             "y: " + str(y_connection_a) + "\n" +
                                             "z: " + str(z_connection_a))

        if connection_b_active and (not plane.are_coordinates_legal(x_connection_b, y_connection_b, z_connection_b)):
            raise BadInitializationException("There was an attempt to set connection coordinates that are outside the matrix for track " +
                                             name + " Coordinates:\n" +
                                             "x: " + str(x_connection_b) + "\n" +
                                             "y: " + str(y_connection_b) + "\n" +
                                             "z: " + str(z_connection_b))

        length_active = False
        if length != 0:
            length_active = True

        good_combinations_found = False

        if pos_active and length_active:
            good_combinations_found = True
            calc_x_connection_a, calc_y_connection_a, calc_z_connection_a = Calculations.point_after_rotation_and_inclination_around_center(xpos, ypos, zpos, length / 2, rot, inclination)
            calc_x_connection_b, calc_y_connection_b, calc_z_connection_b = Calculations.point_after_rotation_and_inclination_around_center(xpos, ypos, zpos, length / 2, -rot, -inclination)

            if connection_a_active:
                x_in_tolerance, diff_x_1 = Calculations.is_in_tolerance(calc_x_connection_a, x_connection_a)
                y_in_tolerance, diff_y_1 = Calculations.is_in_tolerance(calc_y_connection_a, y_connection_a)
                z_in_tolerance, diff_z_1 = Calculations.is_in_tolerance(calc_z_connection_a, z_connection_a)
                if not (x_in_tolerance, y_in_tolerance, z_in_tolerance):
                    exception_text = ("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                      "the calculated connection 1 out of the given track center point, it's rotation and inclination "
                                      "was more off than allowed. The allowed tolerance can be checked in the constants.ini file under "
                                      "tolerances/user_inputs bad combination:\n")
                    if x_in_tolerance:
                        exception_text = exception_text + "x1: " + str(diff_x_1) + "%\n"
                    if y_in_tolerance:
                        exception_text = exception_text + "y1: " + str(diff_y_1) + "%\n"
                    if z_in_tolerance:
                        exception_text = exception_text + "z1: " + str(diff_z_1) + "%\n"

                    raise BadInitializationException(exception_text)
            else:
                x_connection_a = calc_x_connection_a
                y_connection_a = calc_y_connection_a
                z_connection_a = calc_z_connection_a


            if connection_b_active:
                x_in_tolerance, diff_x_2 = Calculations.is_in_tolerance(calc_x_connection_b, x_connection_b)
                y_in_tolerance, diff_y_2 = Calculations.is_in_tolerance(calc_y_connection_b, y_connection_b)
                z_in_tolerance, diff_z_2 = Calculations.is_in_tolerance(calc_z_connection_b, z_connection_b)
                if not (x_in_tolerance, y_in_tolerance, z_in_tolerance):
                    exception_text = ("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                      "the calculated connection 2 out of the given track center point, it's rotation and inclination "
                                      "was more off than allowed. The allowed tolerance can be checked in the constants.ini file under "
                                      "tolerances/user_inputs bad combination:\n")
                    if x_in_tolerance:
                        exception_text = exception_text + "x2: " + str(diff_x_2) + "%\n"
                    if y_in_tolerance:
                        exception_text = exception_text + "y2: " + str(diff_y_2) + "%\n"
                    if z_in_tolerance:
                        exception_text = exception_text + "z2: " + str(diff_z_2) + "%\n"

                    raise BadInitializationException(exception_text)
            else:
                x_connection_b = calc_x_connection_b
                y_connection_b = calc_y_connection_b
                z_connection_b = calc_z_connection_b


        if connection_a_active and connection_b_active and not good_combinations_found:
            good_combinations_found = True

            calculated_length = Calculations.distance_between_two_points(x_connection_a, y_connection_a, z_connection_a,
                                                                         x_connection_b, y_connection_b, z_connection_b)
            if length_active:
                in_tolerance, diff = Calculations.is_in_tolerance(calculated_length, length)
                if not in_tolerance:
                    raise BadInitializationException("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                                     "the calculated length " + str(calculated_length) + " was outside the difference tolerance of the "
                                                     "given range " + str(length))
            else:
                length = int(calculated_length)


            calculated_rot, calculated_inclination = Calculations.rotation_and_inclination_between_two_points(
                x_connection_a, y_connection_a, z_connection_a,
                x_connection_b, y_connection_b, z_connection_b)

            if rot_active:
                in_tolerance, diff = Calculations.is_in_tolerance(calculated_rot, rot)
                if not in_tolerance:
                    raise BadInitializationException("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                                     "the calculated rotation " + str(calculated_rot) + " was outside the difference tolerance of the "
                                                     "given range " + str(rot))
            else:
                rot = calculated_rot

            if inclination != 0:
                in_tolerance, diff = Calculations.is_in_tolerance(calculated_inclination, inclination)
                if not in_tolerance:
                    raise BadInitializationException("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                                     "the calculated inclination " + str(calculated_inclination) + " was outside the difference tolerance of the "
                                                     "given range " + str(inclination))
            else:
                inclination = calculated_inclination

            calc_xpos, calc_ypos, calc_zpos = Calculations.point_after_rotation_and_inclination_around_center(x_connection_a, y_connection_a, z_connection_a, length/2, rot)

            if xpos is None:
                xpos = calc_xpos
            else:
                if not Calculations.is_in_tolerance(xpos, calc_xpos):
                    raise BadInitializationException("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                                     "the calculated central x value " + str(calc_xpos) + " was outside the difference tolerance of the "
                                                     "given range " + str(xpos))

            if ypos is None:
                ypos = calc_ypos
            else:
                if not Calculations.is_in_tolerance(ypos, calc_ypos):
                    raise BadInitializationException("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                                     "the calculated central y value " + str(calc_ypos) + " was outside the difference tolerance of the "
                                                     "given range " + str(ypos))

            if zpos == 0:
                zpos = calc_zpos
            else:
                if not Calculations.is_in_tolerance(zpos, calc_zpos):
                    raise BadInitializationException("There was an attempt to initialize track " + name + " with a value combination that did not match,"
                                                     "the calculated central z value " + str(calc_zpos) + " was outside the difference tolerance of the "
                                                     "given range " + str(zpos))



        if connection_a_active and rot_active and length_active and not(connection_b_active or pos_active):
            good_combinations_found = True
            x_connection_b, y_connection_b, z_connection_b = Calculations.point_after_rotation_and_inclination_around_center(x_connection_a, y_connection_a, z_connection_a, length, rot, inclination)
            xpos, ypos, zpos = Calculations.point_after_rotation_and_inclination_around_center(x_connection_a, y_connection_a, z_connection_a, length / 2, rot, inclination)

        if connection_b_active and rot_active and length_active and not(connection_a_active or pos_active):
            good_combinations_found = True
            x_connection_a, y_connection_a, z_connection_a = Calculations.point_after_rotation_and_inclination_around_center(x_connection_b, y_connection_b, z_connection_b, length, -rot, -inclination)
            xpos, ypos, zpos = Calculations.point_after_rotation_and_inclination_around_center(x_connection_a, y_connection_a, z_connection_a, length / 2, -rot, -inclination)

        if not good_combinations_found:
            raise BadInitializationException("There was an attempt to initialize the track " + name + " with incompatible coordination combinations")

        joined_track_a_oid = None
        if joined_track_a is not None:
            joined_track_a_oid = joined_track_a.get_oid()

        joined_track_b_oid = None
        if joined_track_b is not None:
            joined_track_b_oid = joined_track_b.get_oid()

        track = Track.create_new(name, plane, int(xpos), int(ypos), int(rot), int(zpos), inclination, track_group, blocked, rasperry_pie,
                                 motor_controller, motor_controller_channel, ina_powersensor, relay, analog, exact, dead, speed_limit)

        new_straight_track = object.__new__(cls)
        new_straight_track.__init__(name, length, int(x_connection_a), int(y_connection_a), int(z_connection_a),int(x_connection_b),int(y_connection_b), int(z_connection_b), track, joined_track_a_oid, joined_track_b_oid)
        return new_straight_track

    def copy(self):
        pass
    """
    END public general functions
    """



    """
    START public specific functions
    """
    def switch_to_analog(self):
        print("Noch nicht implementiert StraughtTrack.switch_to_analog")

    def switch_to_digital(self):
        print("Noch nicht implementiert StraughtTrack.switch_to_digital")
    """
    END public specific functions
    """