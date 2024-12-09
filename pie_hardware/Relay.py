import inspect
from typing import override

from core.ClassBase import ClassBase
from core.ClassType import ClassType
#import RPi.GPIO as GPIO
from core.Exceptions import GPIOException, BadInitializationException


class Relay(ClassBase):
    __gpio: int
    __closed: bool

    def __init__(self, gpio: int, closed: bool, oid: str = None):
        """
        Initialize the Relay, pin can be set later
        :param gpio: The GPIO that will be controlling this relay,
         address automatically compensates for I2C pins blocking GPIO 2 and 3
        :param closed: set true to close the relays
        :param oid: to set an already existing oid, ONLY to use when reloading the relay from the database
        :return: nothing
        """
        caller_stack= inspect.stack()
        legal_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_call = True
            if not legal_call:
                raise BadInitializationException("There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.RELAY, oid)
        else:
            super().__init__(ClassType.RELAY)

        self.__is_valid_gpio_address(gpio)
        if gpio > 1:
            gpio = gpio + 2
        self.__gpio = gpio
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.__gpio, GPIO.OUT)
        #if closed:
            #GPIO.output(self.__gpio, GPIO.LOW)
        #else:
            #GPIO.output(self.__gpio, GPIO.HIGH)
        self.__closed = closed

        if str is not None and legal_call:
            self.write_to_db()

    @staticmethod
    def __is_valid_gpio_address(gpio_pin: int):
        """
        Check if the given pin address is valid, throws exception if not
        :param gpio_pin: The GPIO that will be controlling this relay
        :return: nothing
        """
        if 1 <= gpio_pin <= 24:
            return True
        else:
            raise GPIOException("Attempt to set a GPIO outside of the possible range from 1 to 24")

    def close(self):
        """
        Sets the relay closed by setting the GPIO to HIGH
        :return: nothing
        """
        GPIO.output(self.__gpio, GPIO.LOW)
        self.__closed = True

    def open(self):
        """
        Sets the relay open by setting the GPIO to LOW
        :return: nothing
        """
        GPIO.output(self.__gpio, GPIO.HIGH)
        self.__closed = False

    def is_closed(self):
        """
        returns true in the relay is closed
        :return: true if the relay is closed
        """
        return self.__closed

    def shutdown(self):
        """
        Cleans the gpio up, to avoid "already in use" warnings on reinitializing, only to be used at the end of a program
        :return: nothing
        """
        GPIO.cleanup()

    @override
    def db_build_class(self, data):
        """
        puts the given parameter in this relay object, only to be used by the database to load an already existing relay
        from the database, to create a new relay, use the constructor directly and NEVER set the parameter "oid"
        :return: the Relay object with the given parameter
        """
        return Relay(int(data[1]), data[2], data[0])

    @override
    def write_to_db(self):
        print("Implementation missing")
        #TODO Implement
