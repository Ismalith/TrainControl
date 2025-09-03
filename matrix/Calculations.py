import math
from typing import Union

from core.Exceptions import MathException
from core.Tools import Tools


class Calculations:
    @classmethod
    def point_after_rotation_and_inclination_around_center(cls, x_center, y_center, z_center, distance, rotation = 0.0, inclination = 0.0) -> tuple[float, float, float]:
        """
        Takes the center point of the rotation, sets another point in the given distance, to the center point and rotates it
        at first in z direction with the inclination and then on the flat with x, y and returns the coordinates
        in x, y, z order
        :param x_center: x coordinate from the center point
        :param y_center: y coordinate from the center point
        :param z_center: z coordinate from the center point
        :param distance: the distance of the new added point to the center point
        :param rotation: the rotation of the new added point around the center point on the flat x, y
        :param inclination: the inclination of the new added point over the center point on the height z, inclination is always given in per mill not percent
        """
        beta = cls.inclination_to_radius(inclination)
        b = math.sin(math.radians(beta)) / (math.sin(math.radians(90)) / distance)
        a = math.sqrt((distance ** 2) - (b ** 2))

        x1pos = a * math.cos(math.radians(rotation)) + x_center
        y1pos = a * math.sin(math.radians(rotation)) + y_center
        z1pos = z_center + b

        return x1pos, y1pos, z1pos



    @classmethod
    def distance_between_two_points(cls, x1, y1, height1, x2, y2, height2) -> float:
        """
        Returns the distance between two points in the matrix, direction or which point is given first and second is irrelevant
        :param x1: x coordinate from point 1
        :param y1: y coordinate from point 1
        :param height1: the height of point 1, mathematically this is the z coordinate of point 1
        :param x2: x coordinate from point 2
        :param y2: y coordinate from point 2
        :param height2: the height of point 2, mathematically this is the z coordinate of point 2
        """
        return math.sqrt(((x1-x2) ** 2) + ((y1 - y2) ** 2) + ((height1 - height2) ** 2))



    @classmethod
    def rotation_and_inclination_between_two_points(cls, x1, y1, height1, x2, y2, height2):
        """
        Returns the inclination in per mill between the two given points in the matrix
        :param x1: x coordinate from point 1
        :param y1: y coordinate from point 1
        :param height1: the height of point 1, mathematically this is the z coordinate of point 1
        :param x2: x coordinate from point 2
        :param y2: y coordinate from point 2
        :param height2: the height of point 2, mathematically this is the z coordinate of point 2
        """
        c_inc = Calculations.distance_between_two_points( x1, y1, height1, x2, y2, height2)
        b_inc = height2 - height1
        beta_inc = math.degrees(math.asin(b_inc/c_inc)) #TODO Holk, irgendwie gibts hier einen divide by Zero Fehler bei der teststrecke 3
        inclination = Calculations.radius_to_inclination(beta_inc)

        a_rot = x2 - x1
        b_rot = y2 - y1
        rotation = math.degrees(math.atan2(b_rot,a_rot))
        if rotation < 0:
            rotation = rotation + 360
        return rotation, inclination



    @classmethod
    def radius_to_inclination(cls, radius) -> float:
        """
        Converts the given radius in per mill into inclination in percent
        :param radius: The radius, that is to be converted
        """
        return (math.tan(math.radians(radius)) * 100) * 10



    @classmethod
    def inclination_to_radius(cls, inclination) -> float:
        """
        Converts the given inclination in percent into radius
        :param inclination: The inclination in per mill, that is converted into a radius
        """
        return math.degrees(math.atan((inclination/10) / 100))



    @classmethod
    def is_in_tolerance(cls, base_value, test_value) -> tuple[bool, float]:
        """
        Checks if the two values are within the allowed distance of each other, the allowed distance is given by the
        constants.ini file by the "user_inputs" value in the "tolerances" section
        :param base_value: the first and base value
        :param test_value: the second value and that is tested, if it is close enough to the base value
        """
        tolerances = Tools.ini_reader("/track/", "constants.ini", "tolerances")
        tolerance_factor = tolerances["user_inputs"]
        difference = abs(base_value - test_value)
        diff_in_percent = difference / (base_value / 100)

        if diff_in_percent > tolerance_factor:
            return False, diff_in_percent
        return True, 0.0



    @classmethod
    def scaled_kmh_to_real_ms(cls,kmh : Union[int, float]): #TODO HOLK Das hier schränkt das Programm auf H0, es sollten alle Spuren möglich sein auch noch nicht bekannte
        """ #TODO HOLK AM Besten wäre es, eine eigene Tabelle in der Datenbank an legen zu lassen, die die eigene Spur, und in Zukunft vielleicht noch andere generelle Infos, z.b. Speichername der Strecke oder so beinhaltet
        Converts the scaled km/h for the track to the real m/s speed #TODO HOLK, die Standartspuren sind im generatldata.ini bereits mit Name und Scale angelegt
        :param kmh: the scaled speed that the real train with its real size would have
        """
        return (kmh / 87.0) / 3.6


    @classmethod
    def real_ms_to_scaled_kmh(cls,ms : Union[int, float]):#TODO HOLK Das hier schränkt das Programm auf H0, es sollten alle Spuren möglich sein auch noch nicht bekannte
        """ #TODO HOLK AM Besten wäre es, eine eigene Tabelle in der Datenbank an legen zu lassen, die die eigene Spur, und in Zukunft vielleicht noch andere generelle Infos, z.b. Speichername der Strecke oder so beinhaltet
        Converts the real m/s speed for the track to the scaled km/h #TODO HOLK, die Standartspuren sind im generatldata.ini bereits mit Name und Scale angelegt
        :param ms: the real speed that the model train actually has
        """
        return (ms * 3.6) * 87.0