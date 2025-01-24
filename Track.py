from pie_hardware.Ina219PowerSensor import Ina219PowerSensor
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import TrackException
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller
from pie_hardware.Relay import Relay


class Track(ClassBase):
    """
    Controls of a section of the track
    """
    __address: int
    __relay: Relay
    __power_sensor: Ina219PowerSensor
    __motor_controller: M3HMotorcontroller
    __reserved: bool

    def __init__(self, name: str, address: int, motor_controller: M3HMotorcontroller, oid:str = None):
        """
        Initialize track section with its motor controller, relay and sensor
        :param address:
        """
        super().__init__(ClassType.TRACK)
        if 1 <= address <= 3:
            self.__address = address
        else:
            raise TrackException("Attempt to initialize a Track with a number that is outside the range from 1 to 30")
        self.__motor_controller = motor_controller
        self.__relay = Relay(address)

        #self.__power_sensor = Ina219PowerSensor(hier die Adressen rausfinden)

    def run(self, speed: int, acceleration: int, deceleration: int):
        self.__relay.close()
        print(self.__address)
        self.__motor_controller.run_forward(self.__address, speed, acceleration, deceleration)

    def shutdown(self):
        self.__relay.open()

    def reset(self):
        self.__motor_controller.reset()
