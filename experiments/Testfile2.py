import helper.DatabaseOrga
from database.Database import Database
from pie_hardware.Relay import Relay

#helper.DatabaseOrga.reset_db_tables()
object : Relay
object = Database.get_object("REL9361950")
print(object)
if object is not None:
    print(object.get_type(), object.get_oid(), object.is_closed())