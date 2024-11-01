import random

from core.ClassType import ClassType
from core.Exceptions import BadInitializationException


class ClassBase:
    """
    All persistent classes have to inherit from this class,
    it organizes the synchronization of classes and the database
    """
    __oid = "xxx"
    __classType: ClassType

    def __init__(self, class_type: ClassType):
        """
        Base initialization for all persistent classes, sets the oid and the type of the created class
        :param class_type: the class type to identify the new class
        """
        if self.__oid != "xxx":
            raise BadInitializationException("Attempt to initialize a class that was already initialized")

        self.__oid = class_type.value + "-" + str(random.randint(1000000000, (1000000000 * 10 - 1)))
        globals()['classType'] = class_type

    def get_oid(self):
        """
        Returns the oid of this class
        :return: oid
        """
        return self.__oid

    def get_type(self):
        """
        Returns the type of this class
        :return: enum class type
        """
        return self.__classType

    def get_known_classes(self) -> list[object]:
        pass

    def shutdown(self):
        """
        Shutdown procedure for a clean and save exit.
        """
        pass
