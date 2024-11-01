from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadAddressException, M3HMotorcontrollerException
import re
import motoron


class M3HMotorcontroller(ClassBase):
    """
    M3H256 or M3H550 Motor Controller

    The power control for analog locomotives
    """
    __address = -1
    __pins = []
    __error_mask = (
            (1 << motoron.STATUS_FLAG_PROTOCOL_ERROR) |
            (1 << motoron.STATUS_FLAG_CRC_ERROR) |
            (1 << motoron.STATUS_FLAG_COMMAND_TIMEOUT_LATCHED) |
            (1 << motoron.STATUS_FLAG_MOTOR_FAULT_LATCHED) |
            (1 << motoron.STATUS_FLAG_RESET) |
            (1 << motoron.STATUS_FLAG_COMMAND_TIMEOUT)
    )
    __ready = False
    __motorcontroller: motoron.MotoronI2C()
    __direction: dict = {1: 0, 2: 0, 3: 0}

    def __init__(self, address):
        """
        Initialize the M3HMotorcontroller converter on the given hex address
        :param address: the hex address for the M3H motor controller
        :return: nothing
        """
        if re.fullmatch(r'^[0-9a-fA-F]+$', str(address)):
            self.__address = hex(address)
        else:
            raise BadAddressException("Attempt to initialize a M3HMotorcontroller converter with a non hex address")
        self.__motorcontroller = motoron.MotoronI2C(address=int(self.__address, 16))
        super().__init__(ClassType.M3HMOTORCONTROLLER)

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
        self.__motorcontroller.set_error_response(motoron.ERROR_RESPONSE_COAST)
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
            raise M3HMotorcontrollerException("Attempt to set the forward target speed for " + self.get_oid() + " id "
                                              + str(channel) + " to above 800 or below 0, set value was "
                                              + str(target_speed))

        if -1 > starting_speed > 800:
            raise M3HMotorcontrollerException("Attempt to set the starting speed for " + self.get_oid() + " id "
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
            raise M3HMotorcontrollerException("Attempt to set the target speed for " + self.get_oid() + " id "
                                              + str(channel) + " to above 800 or below 0, set value was "
                                              + str(target_speed))

        if -1 > starting_speed > 800:
            raise M3HMotorcontrollerException("Attempt to set the starting speed for " + self.get_oid() + " id "
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
            raise M3HMotorcontrollerException("Attempt to set the speed for" + self.get_oid() + " id "
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
            raise M3HMotorcontrollerException("M3H motor controller " + self.get_oid() + " has to be reset before use")

        if not 1 <= chanel <= 3:
            raise M3HMotorcontrollerException("Attempt to drive the motor controller " + self.get_oid()
                                              + " with an id outside of the 1-3 range: " + chanel)
