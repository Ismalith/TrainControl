#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadAddressException, Ina219AmpSensException
import re


class Ina219PowerSensor(ClassBase):
    """
    INA219 Power Sensor

    The sensor to measure if a locomotive is on a part of the track and the current demanded power
    """
    __MAX_EXPECTED_AMPS = 2.0
    __SHUNT_OHMS = 0.1
    __address = -1
    __pins = []

    def __init__(self, address):
        """
        Initialize the Ina219 converter with a hex address
        :param address: the hex address for the Ina219 chip
        :return: nothing
        """
        if re.fullmatch(r'^[0-9a-fA-F]+$', str(address)):
            self.__address = hex(address)
        else:
            raise BadAddressException("Attempt to initialize an Ina219AmpSensor converter with a non hex address")
        super().__init__(ClassType.INA219AMPSENS)

    def read_current(self):
        """
        Reads the current on the chip in amps
        :return: the current in amps
        """
        ina219 = INA219(self.__SHUNT_OHMS, self.__MAX_EXPECTED_AMPS, address=int(self.__address, 16))
        ina219.configure(ina219.RANGE_32V, ina219.GAIN_8_320MV)
        try:
            return "%.1f" % (ina219.current() / 1000)
        except DeviceRangeError:
            raise Ina219AmpSensException("Current overflow at Ina219AmpSensor " + self.__address)

    def read_power(self):
        """
        Reads the power on the chip in full watts
        :return: the power in watts
        """
        ina219 = INA219(self.__SHUNT_OHMS, self.__MAX_EXPECTED_AMPS, address=int(self.__address, 16))
        ina219.configure(ina219.RANGE_32V, ina219.GAIN_8_320MV)
        try:
            return "%.1f" % (ina219.power() / 1000)
        except DeviceRangeError:
            raise Ina219AmpSensException("Current overflow at Ina219AmpSensor " + self.__address)
