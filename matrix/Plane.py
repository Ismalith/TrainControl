import inspect
from typing import override
import numpy as np
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Exceptions import BadInitializationException, MatrixAndPlaneException
from database.Database import Database
from matrix.Matrix import Matrix


class Plane(ClassBase):
    """
    Matrix

    A plane that contains the actual objects of a track like rails and signals
    """
    __matrix:Matrix
    __xlength:int
    __ylength:int
    __xpos:int
    __ypos: int
    __zpos: int
    __xrot:int
    __yrot: int
    __zrot: int



    """
    START create functions
    """
    def __init__(self, name:str, xlength:int, ylength:int, xpos:int, ypos:int, zpos:int, xrot:int, yrot:int, zrot:int, matrix:Matrix = None, oid:str = None):
        """
        Initialize the Plane, do not use manually
        """
        caller_stack = inspect.stack()
        legal_db_call = False
        if oid is not None:
            for line in caller_stack:
                if "Database.py" in str(line):
                    legal_db_call = True
            if not legal_db_call:
                raise BadInitializationException(
                    "There was an attempt to set an oid manually, this is ONLY allowed for the database to load already constructed classes")
            super().__init__(ClassType.PLANE, name, oid)
        else:
            super().__init__(ClassType.PLANE, name)

        self.__matrix = matrix
        self.__xlength = xlength
        self.__ylength = ylength
        self.__xpos = xpos
        self.__ypos = ypos
        self.__zpos = zpos
        self.__xrot = xrot
        self.__yrot = yrot
        self.__zrot = zrot

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
        Puts the given parameter in this Plane object, only to be used by the database to load an already existing plane
        from the database, to create a new plane, use the constructor directly and NEVER set the parameter "oid"
        :return: the Plane object with the given parameter
        """
        new_plane = object.__new__(cls)
        new_plane.__init__(data[1], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[2], data[0])
        return new_plane


    @override
    def __db_write_to_db__(self):
        dimensions = self.get_dimensions()
        position = self.get_position()
        rotation = self.get_rotation()
        if self.get_matrix() is not None:
            sql_insert = ("INSERT INTO plane (oid, name, matrix, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot) VALUES ('"
                          + self.get_oid() + "', '" + self.get_name() + "', '" + str(self.get_matrix().get_oid()) + "', '" +
                          str(dimensions[0]) + "', '" + str(dimensions[1]) + "', '" +
                          str(position[0]) + "', '" + str(position[1]) + "', '" + str(position[2]) + "', '" +
                          str(rotation[0]) + "', '" + str(rotation[1]) + "', '" + str(rotation[2]) + "')")
            Database.run_sql_query(sql_insert, False)
        else:
            sql_insert = ("INSERT INTO plane (oid, name, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot) VALUES ('"
                          + self.get_oid() + "', '" + self.get_name() + "', '" + str(dimensions[0]) + "', '" +
                          str(dimensions[1]) + "', '" + str(position[0]) + "', '" + str(position[1]) + "', '" +
                          str(position[2]) + "', '" + str(rotation[0]) + "', '" + str(rotation[1]) + "', '" +
                          str(rotation[2]) + "')")
            Database.run_sql_query(sql_insert, False)
    """
    END db functions
    """



    """
    START public general functions
    """
    @classmethod
    def create_new(cls, name:str = None, xlength:int = 0, ylength:int = 0, xpos:int = -1, ypos:int = -1, zpos:int = 0, xrot:int = 0, yrot:int = 0, zrot:int = 0, ):
        """
        Creation methode to create and write a new plane to the database, only create new lane with this method, the matrix is added automatically if one exists,
        if none exists the plane can itself be the base object however this only allows one plane and a matrix can not be added after the fact
        :param name: the name for the plane, if not chosen manually the new relay will get the name "Plane 1"
        :param xlength: the length of the plane in µm (1/10000)
        :param ylength: the width of the plane in µm (1/10000)
        :param xpos: the x position of the center of the plane in the matrix in µm (1/10000)
        :param ypos: the y position of the center of the plane in the matrix in µm (1/10000)
        :param zpos: the horizontal position of the center of the plane in the matrix in µm (1/10000)
        :param xrot: the rotation around the x-axis of the center of the plane in the matrix in µm (1/10000)
        :param yrot: the rotation around the y-axis of the center of the plane in the matrix in µm (1/10000)
        :param zrot: the rotation around the z-axis of the center of the plane in the matrix in µm (1/10000)
        :return: the newly created plane
        """
        if name is None:
            highest_generic_name = Database.run_sql_query("SELECT name FROM plane WHERE name ~ '^plane \\d+$' ORDER BY name DESC LIMIT 1")
            if highest_generic_name is not None:
                name = "Plane " + str(int(str(highest_generic_name).rsplit(" ")[1]) + 1)
            else:
                name = "Plane 1"
        else:
            found_planes = int(Database.run_sql_query("SELECT count(oid) FROM plane WHERE name = '" + name + "'"))
            if found_planes > 0:
                raise BadInitializationException("A planes pie with the name " + name + " is already in the database")


        if xlength < 0 or ylength < 0:
            raise BadInitializationException("There was an attempt to create a new Plane object with one of it's dimensions smaller than 1:\n"
                                             "X length = " + str(xlength) + "\n"
                                             "z length = " + str(ylength) + "\n")

        if xpos < -1 or ypos < -1 or zpos < 0:
            raise BadInitializationException("There was an attempt to create a new Plane object with a starting point with negative coordinates:\n"
                                             "X pos = " + str(xpos) + "\n"
                                             "Y pos = " + str(ypos) + "\n"
                                             "Z pos = " + str(zpos) + "\n")

        if xrot < -90 or yrot < -360 or zrot < -90:
            raise BadInitializationException("There was an attempt to create a new Plane object with a rotation outside of the negative rotation limits:\n"
                                             "The rotation limits are x = -90°, y = -360°, z = -90°:\n"
                                             "X rotation = " + str(xrot) + "\n"
                                             "Y rotation = " + str(yrot) + "\n"
                                             "Z rotation = " + str(zrot) + "\n")

        if xrot > 90 or yrot > 90 or zrot > 359:
            raise BadInitializationException("There was an attempt to create a new Plane object with a rotation outside of the rotation limits\n"
                                             "The rotation limits are x = 90°, y = 90°, z = 359°:\n"
                                             "X rotation = " + str(xrot) + "\n"
                                             "Y rotation = " + str(yrot) + "\n"
                                             "Z rotation = " + str(zrot) + "\n")


        matrix:Matrix = Database.get_object_for_oid(Database.run_sql_query("SELECT oid FROM matrix"))

        if matrix is None:
            if xpos == -1 and ypos == -1 and ypos == -1 and xrot == 0 and yrot == 0 and zrot == 0:
                new_plane = object.__new__(cls)
                new_plane.__init__(name, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot, None)
                return  new_plane
            else:
                raise BadInitializationException("There was an attempt to create a plane that hat rotation or position values given while there was not matrix defined, "
                                                 "to define a plane without a matrix position and rotation parameter must be empty, "
                                                 "if the plane should be within a matrix the matrix needs to be created first.")

        if xlength == 0:
            xlength = matrix.get_dimensions()[0]

        if ylength == 0:
            ylength = matrix.get_dimensions()[1]

        if xpos == -1:
            xpos = int(matrix.get_dimensions()[0] / 2)

        if ypos == -1:
            ypos = int(matrix.get_dimensions()[1] / 2)


        corner_1 = [0, 0, 0]
        corner_2 = [xlength, 0, 0]
        corner_3 = [0, ylength, 0]
        corner_4 = [xlength, ylength, 0]
        four_corners = [corner_1, corner_2, corner_3, corner_4]

        for corner in four_corners:
            absolute_point = Plane.__get_absolute_position_in_matrix(corner[0], corner[1], corner[2], xpos, ypos, zpos, xrot, yrot, zrot)
            if absolute_point[0] < 0 or absolute_point[1] < 0 or absolute_point[2] < 0:
                raise BadInitializationException("Attempt to create a new plane with at least one point outside the matrix, found point:\n" +
                                                 str(corner[0]) + "|" + str(corner[1]) + " (" + str(absolute_point[0]) + "|" + str(absolute_point[1]) + "|" + str(absolute_point[2]) + ")")

        new_plane = object.__new__(cls)
        new_plane.__init__(name, xlength, ylength, xpos, ypos, zpos, xrot, yrot, zrot, matrix)
        return new_plane


    @override
    def save(self):
        """
        Saves the current state of this matrix into the database
        """
        print("Noch nicht implementiert Matrix.save")


    def shutdown(self):
        """
        Cleans the matrix object up
        :return: nothing
        """
        self.__db_write_to_db__()
    """
    END public general functions
    """



    """
    START private specific functions
    """
    @classmethod
    def __get_absolute_position_in_matrix(cls, x:int, y:int, z:int, xpos:int, ypos:int, zpos:int, xrot:int = 0, yrot:int = 0, zrot:int = 0) -> tuple[int, int, int]:
        xrad = np.radians(float(xrot))
        yrad = np.radians(float(yrot))
        zrad = np.radians(float(zrot))
        point = np.array([float(x), float(y), float(z)])

        rot_matrix_x = np.array([
            [1, 0, 0],
            [0, np.cos(xrad), -np.sin(xrad)],
            [0, np.sin(xrad), np.cos(xrad)]
        ])

        rot_matrix_y = np.array([
            [np.cos(yrad), 0, -np.sin(yrad)],
            [0, 1, 0],
            [np.sin(yrad), 0, np.cos(yrad)]
        ])

        rot_matrix_z = np.array([
            [np.cos(zrad), -np.sin(zrad), 0],
            [np.sin(zrad), np.cos(zrad), 0],
            [0, 0, 1]
        ])

        rot_point = rot_matrix_z @ (rot_matrix_y @ (rot_matrix_x @ point))
        return int(rot_point[0] + xpos), int(rot_point[1] + ypos), int(rot_point[2] + zpos)


    def __matrix_exists(self, method_name:str):
        if self.__matrix is None:
            raise MatrixAndPlaneException("Attempt to use " + method_name + " while there is no matrix set")
    """
    END private specific functions
    """



    """
    START public specific functions
    """
    def get_matrix(self):
        """
        Returns the matrix in which this plane is
        """
        self.__matrix_exists("get_matrix")
        return self.__matrix


    def get_dimensions(self):
        """
        Returns the x and y dimensions for this plane
        """
        return [self.__xlength, self.__ylength]


    def get_position(self):
        """
        Returns the x, y and z position of this plane in the matrix, the point returned is the center of the plane
        """
        self.__matrix_exists("get_position")
        return [self.__xpos, self.__ypos, self.__zpos]


    def get_rotation(self):
        """
        Returns the x, y and z rotation of this plane in the matrix, the rotation point returned is in the center of the plane
        """
        self.__matrix_exists("get_rotation")
        return [self.__xrot, self.__yrot, self.__zrot]


    def get_absolute_position_in_matrix(self, x:int, y:int, z:int = 0) -> tuple[int, int, int]:
        """
        Returns the absolute position in the matrix for the given point on the plane
        :param x: the x coordinate on the plane that will be translated to its absolute position in the matrix
        :param y: the y coordinate on the plane that will be translated to its absolute position in the matrix
        :param z: the z coordinate on the plane that will be translated to its absolute position in the matrix, if the given point is directly on the plane, it can be left empty
        """
        self.__matrix_exists("get_absolute_position_in_matrix")
        if z == 0:
            return Plane.__get_absolute_position_in_matrix(x, y, z, self.__xpos, self.__ypos, self.__zpos, self.__xrot, self.__yrot, self.__zrot)
        else:
            return Plane.__get_absolute_position_in_matrix(x, y, 0, self.__xpos, self.__ypos, self.__zpos, self.__xrot, self.__yrot, self.__zrot)


    def is_point_in_boarders(self, x:int, y:int):
        """
        Returns true if the given point is within the limits of the plane and false if not
        :param x: the x coordinate of the point to be tested
        :param y: the y coordinate of the point to be tested
        """
        self.__matrix_exists("is_position_in_matrix")
        if self.__xlength > x > 0 and self.__ylength > y > 0:
            return True
        else:
            return False


    def are_coordinates_legal(self, x:int, y:int, z:int):
        """
        Returns true, if the given coordinate is within the containing matrix
        :param x: the x value of the coordinate that is to be tested
        :param y: the y value of the coordinate that is to be tested
        :param z: the z value of the coordinate that is to be tested
        """
        self.__matrix_exists("_are_coordinates_legal")
        x2, y2, z2 = self.get_absolute_position_in_matrix(x, y, z)
        return self.__matrix.point_in_boarders(x2, y2, z2)
    """
    END public specific functions
    """