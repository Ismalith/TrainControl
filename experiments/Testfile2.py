import math
from operator import contains

import database.DatabaseOrga
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from core.Tools import Tools
from database.Database import Database
from matrix.Calculations import Calculations
from matrix.Plane import Plane
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller
from pie_hardware.RasperryPie import RasperryPie
from pie_hardware.Relay import Relay
from track.Track import Track

#from actions.Actions import Actions

#testmotorcontroller = Database.get_object_for_oid("MAT2539060")
#Actions.create_track(radius=350, name="test", rasperry="main", ina219powersensor="test", relay="test", motorcontroller="test")
#test_plane:Plane = Database.get_object_for_oid("PLA4044668")
#print(test_plane)

#print(test_plane.get_absolute_position(50,20))
#print(test_plane.get_absolute_position(2, 1))

#rpi = RasperryPie.create_new(name = "test 1")

#rp = RasperryPie.get_for_id("main")
#print(rp)
#print(Database.get_object_for_oid(rp.get_oid()))

#rp = Database.get_object_for_oid("RAS8787007")
#rp.__delete_my_gpio_connections__()
#rp.__delete_my_i2c_connections__()

#testtrack = Database.get_object_for_name("Test Track 2", ClassType.TRACK)


#xpos= 120
#ypos= 80
#zpos = 5

#rot = 410
#length = 300

#incline = 3


#alpha = 90 - incline
#b = math.sin(math.radians(incline)) / (math.sin(math.radians(90)) / (length/2))
#a = math.sqrt((length/2 * length/2) - (b * b))

#z1pos = zpos + b

#x2pos = a * math.cos(math.radians(rot/10)) + xpos
#y2pos = a * math.sin(math.radians(rot/10)) + ypos

#print("(" + str(x2pos) + "|" + str (y2pos) + "|" + str(z1pos) + ")")

#print(140.954*math.cos(math.radians(41)) + 120)
#print(140.954*math.sin(math.radians(41)) + 80)
#print(math.sin((math.radians(0))))

#x1, y1, z1 = Calculations.point_after_rotation_and_inclination_around_center(120, 80, 30, 150, 41,0)
#x2, y2, z2 = Calculations.point_after_rotation_and_inclination_around_center(120, 80, 20, 150, 221,0)
#print("(" + str(x1) + "|" + str(y1) + "|" + str(z1) + ")")
#print("(" + str(x2) + "|" + str(y2) + "|" + str(z2) + ")")

#base_percent = 90
#angle_after_conversion = Calculations.percent_inclination_to_radius(base_percent)
#print("base_percent: " + str(base_percent) + ", angle_after_conversion: " + str(angle_after_conversion))

#print(Calculations.distance_between_two_points(x1, y1, z1,x2, y2, z2))
#print(Calculations.rotation_and_inclination_between_two_points(120, 80, 0,x2, y2, z2))

print(Database.get_object_for_oid('STR2557606'))