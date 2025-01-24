from operator import contains

import database.DatabaseOrga
from core.ClassBase import ClassBase
from core.ClassType import ClassType
from database.Database import Database
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller
from pie_hardware.RasperryPie import RasperryPie
from pie_hardware.Relay import Relay

#from actions.Actions import Actions

#database.DatabaseOrga.reset_db_tables()

#Actions.create_track(radius=350, name="test", rasperry="main", ina219powersensor="test", relay="test", motorcontroller="test")

#rpi = RasperryPie.create_new(name = "test 1")

#rp = RasperryPie.get_for_id("main")
#print(rp)
#print(Database.get_object_for_oid(rp.get_oid()))

#rp = Database.get_object_for_oid("RAS8787007")
#rp.__delete_my_gpio_connections__()
#rp.__delete_my_i2c_connections__()