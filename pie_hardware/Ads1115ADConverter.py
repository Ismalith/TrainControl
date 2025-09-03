import re
from Adafruit_Python_ADS1x15 import Adafruit_ADS1x15

from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadAddressException, Ads1115ADConverterException


class Ads1115ADConverter(ClassBase):
    """
    Ads1115 Analog Digital Converter

    The sensor to measure the input of a transformer
    """
    __adc: None
    __GAIN = 1
    __address = -1
    __pins = []

    def __init__(self, address = None, pin = None):
        """
        Initialize the Ads1115ADConverter, pins can be set later, address must be set here and can't be changed later
        :param address: I2C address of the Ads1115ADConverter has to be hexal, default 0x48
        :param pin: The A0 to A3 pins on the chip with A0 = 0, A1 = 1, A2 = 2, A3 = 3, default ist none
        :return: nothing
        """
        if address == -1:
            self.__address = 0x48
        elif re.fullmatch(r'^[0-9a-fA-F]+$', str(address)):
            self.__address = address
        else:
            raise BadAddressException("Attempt to initialize an Ads1115 AD converter with a non hex address")
        super().__init__(ClassType.ADS1115ADCONVERTER)

        self.set_new_pins(pin)
        self.__adc: Adafruit_ADS1x15.ADS1115()

    def set_new_pins(self, pins=None):
        """
        Reset pins or first set if they haven't been set yet
        :param pins: The A0 to A3 pins on the chip with A0 = 0, A1 = 1, A2 = 2, A3 = 3, default ist none
        :return: nothing
        """
        if pins is not None:
            new_pins = []
            for pin in pins:
                if pin == 0 or pin == 1 or pin == 2 or pin == 3:
                    if pin not in new_pins:
                        new_pins.append(pin)
                    else:
                        message = "Attempt to set a pin more than once: "
                        for number in pins:
                            message = message + str(number) + ", "

                        message = message[:-2]
                        raise Ads1115ADConverterException(message)
                else:
                    raise Ads1115ADConverterException(
                        "Attempt to set a pin with something else than a number from 0 to 3: " + str(pin)
                    )
            self.__pins = new_pins

    def read_voltage(self, pin):
        """
        Read the voltage of the given pin, pins have to be initialized before they can be used here
        :param pin: The pin to be read range 0 to 3
        :return: voltage with two decimals accuracy
        """
        if pin in self.__pins:
            return round((self.__adc.read_adc(pin, gain=self.__GAIN) / 4096), 2)
        else:
            raise Ads1115ADConverterException("Attempt to read from a unset pin, Pin: " + str(pin))

    def read_voltage_all(self):
        """
        Read the voltage of all existing pins, pins have to be initialized before they can be used here, voltages are
        returned as a list where the number of the pin (0 to 3) is the key to it's measured voltage
        :return: list of voltages with two decimals accuracy with their pin as key in the list
        """
        voltages = []
        if self.__pins.__len__() > 0:
            for pin in self.__pins:
                voltages.insert(pin, round((self.__adc.read_adc(pin, gain=self.__GAIN) / 4096), 2))
        else:
            raise Ads1115ADConverterException("Attempt to read while no pins are initialized")
