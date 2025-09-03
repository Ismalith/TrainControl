from core.ClassBase import ClassBase
from core.ClassType import ClassType
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller


class TrackGroup(ClassBase):
    """
    Controls of a section of the track
    """
    __motor_controller: M3HMotorcontroller
    __track1: int
    __track2: int
    __track3: int

    def __init__(self, hex, main_address: int, sub_address1: int, sub_address2: int):
        """
        Initialize track section with its motor controller, relay and sensor
        :param main_address:
        :param sub_address1:
        :param sub_address2:
        """
        super().__init__(ClassType.TRACKGROUP)

        self.__motor_controller = M3HMotorcontroller(hex + main_address - 1)
        self.__motor_controller.reset()