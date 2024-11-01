from core.ClassBase import ClassBase
from core.ClassType import ClassType
import RPi.GPIO as GPIO
from core.Exceptions import GPIOException


class Relay(ClassBase):
    __gpio: int
    __closed: bool

    def __init__(self, gpio: int):
        """
        Initialize the Relay, pin can be set later
        :param gpio: The GPIO that will be controlling this relay,
         address automatically compensates for I2C pins blocking GPIO 2 and 3
        :return: nothing
        """
        super().__init__(ClassType.RELAY)
        self.__is_valid_gpio_address(gpio)
        if gpio > 1:
            gpio = gpio + 2
        self.__gpio = gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio, GPIO.OUT)
        GPIO.output(self.__gpio, GPIO.HIGH)
        self.__closed = False

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
