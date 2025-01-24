import inspect
from typing import override
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadAddressException, M3HMotorcontrollerException, BadInitializationException
import re
#import motoron TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
from database.Database import Database
from pie_hardware.RasperryPie import RasperryPie


class M3HMotorcontroller(ClassBase):
    """
    M3H256 or M3H550 Motor Controller

    The power control for analog locomotives
    """
    __address:str
    #__error_mask = ( TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
           #(1 << motoron.STATUS_FLAG_PROTOCOL_ERROR) |
            #(1 << motoron.STATUS_FLAG_CRC_ERROR) |
            #(1 << motoron.STATUS_FLAG_COMMAND_TIMEOUT_LATCHED) |
            #(1 << motoron.STATUS_FLAG_MOTOR_FAULT_LATCHED) |
            #(1 << motoron.STATUS_FLAG_RESET) |
            #(1 << motoron.STATUS_FLAG_COMMAND_TIMEOUT)
    #)
    __ready = False
    #__motorcontroller: motoron.MotoronI2C() TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
    __direction: dict = {1: 0, 2: 0, 3: 0}



    """
    START create functions
    """
    def __init__(self, name:str, rp_pie:RasperryPie, address:str = None, oid:str = None):
        """
        Initialize the M3HMotorcontroller converter, do not use manually
        """
        if not re.fullmatch(r'^0x[0-7][0-9a-fA-F]$', address):
            raise BadAddressException("Attempt to initialize an M3HMotorcontroller converter with a non hex address")

        caller_stack = inspect.stack()
        legal_db_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_db_call = True
            if not legal_db_call:
                raise BadInitializationException("There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.M3HMOTORCONTROLLER, name, oid)
        else:
            super().__init__(ClassType.M3HMOTORCONTROLLER, name)

        self.__rp_pie = rp_pie
        self.__address = address
        #self.__motorcontroller = motoron.MotoronI2C(address=int(self.__address, 16))TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
        if not legal_db_call:
            self.__db_write_to_db__()
    """
    END create functions
    """



    """
    START db functions
    """
    @classmethod
    def __db_build_class__(cls, data):
        """
        Puts the given parameter in this motorcontroller object, only to be used by the database to load an already existing relay
        from the database, to create a new motorcontroller, use the constructor directly and NEVER set the parameter "oid"
        :return: the M3HMotorcontroller object with the given parameter
        """
        new_ina219_sensor = object.__new__(cls)
        new_ina219_sensor.__init__(data[2], data[1], data[3], data[0])
        return new_ina219_sensor

    @override
    def __db_write_to_db__(self):
        if self.__address is not None:
            sql_insert = "INSERT INTO m3hmotorcontroller (oid, name, rasperrypie, i2caddress) VALUES ('" + self.get_oid() + "','" + self.get_name() + "','" + str(self.get_rasperry_pie().get_oid()) + "','" + self.get_address() + "')"
            Database.run_sql_query(sql_insert, False)
        else:
            sql_insert = "INSERT INTO m3hmotorcontroller (oid, name, rasperrypie) VALUES ('" + self.get_oid() + "','" + self.get_name() + "','" + str(self.get_rasperry_pie().get_oid()) + "')"
            Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, rasperry_pie: RasperryPie, address:str = None, name: str = None):
        """
        Creation methode to create and write a new M3HMotorcontroller to the database, only create new M3HMotorcontroller with this method
        :param rasperry_pie: the rasperry pie that is controlling this motor controller
        :param address: the i2c address from the rasperry pie that will be controlling this motor controller,
        :param name: the name for the motor controller, if not chosen manually the new motor controller will get the name "MotorController x" where x is the new highest numer of all existing "MotorController x"
        :return: the newly created motor controller
        """

        if name is None:
            highest_generic_name = Database.run_sql_query("SELECT name FROM m3hmotorcontroller WHERE name ~ '^MotorController \\d+$' ORDER BY name DESC LIMIT 1")
            if highest_generic_name is not None:
                name = "MotorController " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
            else:
                name = "MotorController 1"
        else:
            found_power_sensors_with_same_name = Database.run_sql_query("SELECT count(oid) FROM m3hmotorcontroller "
                "WHERE name = '" + name + "' AND rasperrypie = '" + rasperry_pie.get_oid() + "'")
            if found_power_sensors_with_same_name > 0:
                raise BadInitializationException("A M3H motor controller with the name " + name + " is already in use on the same rasperry pie " + rasperry_pie.get_name())

        if address is not None:
            rasperry_pie.i2c_is_free(address)

        new_m3h_motor_controller = object.__new__(cls)
        new_m3h_motor_controller.__init__(name, rasperry_pie, address)
        return new_m3h_motor_controller


    @override
    def save(self):
        """
        Saves the current state of this rasperry pie into the database
        """
        print("Noch nicht implementiert M3hMotorcontroller.save")


    @override
    def shutdown(self):
        self.__db_write_to_db__()
    """
    END public general functions
    """



    """
    START public specific functions
    """
    def connect_to_i2c(self, rasperry_pie: RasperryPie, address: str):
        """
        Connects this motor controller to the given rasperry pie on the given address after testing if this address is
        valid and free
        :param rasperry_pie: the rasperry pie that this motor controller is to be connected to
        :param address: the i2c address
        """
        rasperry_pie.i2c_is_free(address)
        Database.run_sql_query("UPDATE m3hmotorcontroller SET i2caddress = " + str(address) + " AND rasperrypie = '" +
                               rasperry_pie.get_oid() + "' WHERE oid = '" + self.get_oid() + "'",False)

        self.__rp_pie = rasperry_pie
        self.__address = address


    def get_rasperry_pie(self):
        """
         Returns the rasperry pie that controls this motor controller
         :return: the rasperry pie, that controls this motor controller
         """
        return self.__rp_pie


    def get_address(self):
        """
        The hex address that the rasperry pie uses to control this motor controller
        :return: the address to control this motor controller
        """
        return self.__address


    def reset(self):
        """
        Resets the motor controller including its error flags and makes it ready to run, if a motor is still running
        it won't reset, but it will give a stop command to the motor. In that case just wait until motors are stopped
        :return: true if the reset was successful, false if it failed
        """
        if self.__motorcontroller.get_motor_driving_flag():
            self.__ready = False
            self.__motorcontroller.set_max_deceleration(1, 10)
            self.__motorcontroller.set_max_deceleration(2, 10)
            self.__motorcontroller.set_max_deceleration(3, 10)
            self.__motorcontroller.reset()
            return False

        self.__motorcontroller.reinitialize()
        self.__motorcontroller.clear_reset_flag()
        #self.__motorcontroller.set_error_response(motoron.ERROR_RESPONSE_COAST) TODO sobald auf einem Rasperry Pie, diese Zeilen wieder einfügen
        self.__motorcontroller.set_error_mask(self.__error_mask)
        self.__motorcontroller.set_command_timeout_milliseconds(1000000)
        self.__ready = True
        self.__direction = {1: 0, 2: 0, 3: 0}

    def run_reset_direction(self, channel: int):
        """
        To avoid uncontrolled direction changes, the direction first driven, blocks the other direction from being used,
        this method resets this lock, if the given channel ist at 0 speed
        :param channel: the id of the channel on the M3H controller
        :return: True when reset was successful, False if not
        """
        self.__check_ready_and_controller(channel)
        if self.__motorcontroller.get_current_speed(channel):
            self.__direction[channel] = 0
            return True
        return False

    def run_forward(self, channel: int, target_speed: int, acceleration: int, deceleration: int, starting_speed: int = -1):
        """
        Sets a new forward target speed that the controller will accelerate or slow the train to with the given
        acceleration rate, if target_speed is equal to the current speed of the controller, the speed will just be
        reset to reset the timeout timer of the controller
        can not be used directly after run_backward(), controller direction has to be reset first
        :param channel: the id of the channel on the M3H controller
        :param target_speed: the speed the controller should speed up to
        :param acceleration: the rate speed is increased
        :param deceleration: the rate that speed is decreased
        :param starting_speed: The speed that the controller should start from for acceleration
        :return: nothing
        """
        self.__check_ready_and_controller(channel)

        if self.__direction[channel] == -1:
            raise M3HMotorcontrollerException("Attempt to set a forward speed for " + self.get_oid()
                                              + " while it was in backward mode,"
                                              + " M3H controller have to be reset before changing the direction")
        elif self.__direction[channel] == 0:
            self.__direction[channel] = 1
        elif self.__direction[channel] != 1:
            raise M3HMotorcontrollerException("Attempt to set " + str(self.__direction[channel])
                                              + " for the direction of M3H " + self.get_oid()
                                              + " only -1, 0 and 1 are defined")

        if 0 > target_speed > 800:
            raise M3HMotorcontrollerException("Attempt to set the forward target speed for " + self.get_name() + " name "
                                              + str(channel) + " to above 800 or below 0, set value was "
                                              + str(target_speed))

        if -1 > starting_speed > 800:
            raise M3HMotorcontrollerException("Attempt to set the starting speed for " + self.get_name() + " name "
                                              + str(channel) + " to above 800 or below -1, set value was "
                                              + str(starting_speed))

        if 0 > acceleration > 100 or 0 > deceleration > 100:
            raise M3HMotorcontrollerException("Attempt to set a too aggressive speed change for " + self.get_oid()
                                              + ", do not set values above 100 or below 0, given acceleration was "
                                              + str(acceleration) + " and  given deceleration was " + str(deceleration))

        if starting_speed == target_speed:
            self.__motorcontroller.reset_command_timeout()
            return

        if starting_speed == -1:
            starting_speed = self.read_speed(channel)
        elif starting_speed >= 0:
            self.__motorcontroller.set_starting_speed_forward(channel, starting_speed)

        self.__motorcontroller.set_max_acceleration_forward(channel, acceleration)
        self.__motorcontroller.set_max_deceleration_forward(channel, deceleration)
        self.__motorcontroller.set_starting_speed_forward(channel, starting_speed)
        self.__motorcontroller.set_speed(channel, target_speed)

    def run_backward(self, channel: int, target_speed: int, acceleration: int, deceleration: int, starting_speed: int = -1):
        """
        Sets a new backward target speed that the controller will accelerate or slow the train to with the given
        acceleration rate, if target_speed is equal to the current speed of the controller, the speed will just be
        reset to reset the timeout timer of the controller
        can not be used directly after run_forward(), controller direction has to be reset first
        :param channel: the id of the channel on the M3H controller
        :param target_speed: the speed the controller should speed up to
        :param acceleration: the rate speed is increased
        :param deceleration: the rate that speed is decreased
        :param starting_speed: The speed that the controller should start from for acceleration
        :return: nothing
        """
        self.__check_ready_and_controller(channel)

        if self.__direction[channel] == 1:
            raise M3HMotorcontrollerException("Attempt to set a backward speed for " + self.get_oid()
                                              + " while it was in forward mode," +
                                              " M3H controller have to be reset before changing the direction")
        elif self.__direction[channel] == 0:
            self.__direction[channel] = -1
        elif self.__direction[channel] != -1:
            raise M3HMotorcontrollerException("Attempt to set " + str(self.__direction) + " for the direction of M3H "
                                              + self.get_oid() + " only -1, 0 and 1 are defined")

        if 0 > target_speed > 800:
            raise M3HMotorcontrollerException("Attempt to set the target speed for " + self.get_name() + " name "
                                              + str(channel) + " to above 800 or below 0, set value was "
                                              + str(target_speed))

        if -1 > starting_speed > 800:
            raise M3HMotorcontrollerException("Attempt to set the starting speed for " + self.get_name() + " name "
                                              + str(channel) + " to above 800 or below -1, set value was "
                                              + str(starting_speed))

        if 0 > acceleration > 100 or 0 > deceleration > 100:
            raise M3HMotorcontrollerException("Attempt to set a too aggressive speed change for " + self.get_oid()
                                              + ", do not set values above 100 or below 0, given acceleration was "
                                              + str(acceleration) + " and  given deceleration was " + str(deceleration))

        if starting_speed == target_speed:
            self.__motorcontroller.reset_command_timeout()
            return

        if starting_speed == -1:
            starting_speed = self.read_speed(channel) * -1
        elif starting_speed >= 0:
            self.__motorcontroller.set_starting_speed_reverse(channel, starting_speed)

        self.__motorcontroller.set_max_acceleration_reverse(channel, acceleration)
        self.__motorcontroller.set_max_deceleration_reverse(channel, deceleration)
        self.__motorcontroller.set_starting_speed_reverse(channel, starting_speed)
        self.__motorcontroller.set_speed(channel, target_speed * -1)

    def run_set_track_speed(self, controller_id: int, speed: int):
        """
        Sets the speed of the controller to the given value instantly, must only be used to set a track that is to be
        entered, never use it when a train is on this track, it is likely to get damaged
        :param controller_id: the id of the channel on the M3H controller
        :param speed: the set that the track ist instantly set to
        :return: nothing
        """
        self.__check_ready_and_controller(controller_id)

        if not -800 <= speed <= 800:
            raise M3HMotorcontrollerException("Attempt to set the speed for" + self.get_name() + " name "
                                              + str(controller_id) + " to above 800 or below -800, set value was "
                                              + str(speed) + "\nDANGER: this  warning also  hints at incorrect usage "
                                              + "of this function. It must only be used to set the speed of a track, "
                                              + "that is to be matched to a previous track before being entered")

        self.__motorcontroller.set_speed_now(controller_id, speed)

    def read_speed(self, channel: int):
        """
        Returns the current speed that the controller is set to
        :param channel: the id of the channel on the M3H controller
        :return: nothing
        """
        self.__check_ready_and_controller(channel)
        return self.__motorcontroller.get_current_speed(channel)

    def __check_ready_and_controller(self, chanel: int):
        if not self.__ready:
            raise M3HMotorcontrollerException("M3H motor controller " + self.get_name() + " has to be reset before use")

        if not 1 <= chanel <= 3:
            raise M3HMotorcontrollerException("Attempt to drive the motor controller " + self.get_name()
                                              + " with a channel outside of the 1-3 range: " + chanel)
