import database.DatabaseOrga
from pie_hardware.Ina219PowerSensor import Ina219PowerSensor
from pie_hardware.M3HMotorcontroller import M3HMotorcontroller
from pie_hardware.RasperryPie import RasperryPie
from pie_hardware.Relay import Relay
print("Start reset testdata")
database.DatabaseOrga.reset_db_tables()


print("Start create Rasperry Pies")
main_pie = RasperryPie.create_new("main",True)
sub_pie = RasperryPie.create_new("sub")
db_pie = RasperryPie.create_new("database", database = True)
print("Create Rasperry Pies Done")
print("Start create Relays")
relay_01 = Relay.create_new(name = "REL 1", gpio_pin = 1, rasperry_pie = main_pie)
relay_02 = Relay.create_new(name = "REL 2", gpio_pin = 4, rasperry_pie = main_pie)
relay_03 = Relay.create_new(name = "REL 3", gpio_pin = 5, rasperry_pie = main_pie)
relay_04 = Relay.create_new(name = "REL 4", gpio_pin = 7, rasperry_pie = main_pie)
relay_05 = Relay.create_new(gpio_pin = 8, rasperry_pie = main_pie)
relay_06 = Relay.create_new(10, rasperry_pie = main_pie)
relay_07 = Relay.create_new(12, "Rel an DB", db_pie, True)
relay_08 = Relay.create_new(name = "REL an sub 1", gpio_pin = 1, rasperry_pie = sub_pie)
relay_09 = Relay.create_new(name = "REL an sub 2", gpio_pin = 6, rasperry_pie = sub_pie)
relay_10 = Relay.create_new(name = "REL an sub 3", gpio_pin = 5, rasperry_pie = sub_pie)
relay_11 = Relay.create_new(name = "REL an sub 4", gpio_pin = 7, rasperry_pie = sub_pie)
print("Create Relay Done")
print("Start create Ina219PowerSensor")
power_sensor_01 = Ina219PowerSensor.create_new(name = "PS 1", rasperry_pie = main_pie, address = "0x27")
power_sensor_02 = Ina219PowerSensor.create_new(name = "PS 2", rasperry_pie = main_pie, address = "0x5e")
power_sensor_03 = Ina219PowerSensor.create_new(name = "PS 3", rasperry_pie = main_pie, address = "0x11")
power_sensor_04 = Ina219PowerSensor.create_new(name = "PS 4", rasperry_pie = main_pie, address = "0x60")
power_sensor_05 = Ina219PowerSensor.create_new(name = "PS an DB", rasperry_pie = db_pie, address = "0x27")
power_sensor_06 = Ina219PowerSensor.create_new(sub_pie, name = "PS an Sub 1", address = "0x27")
power_sensor_07 = Ina219PowerSensor.create_new(sub_pie,"0x66","PS and Sub 2")
power_sensor_08 = Ina219PowerSensor.create_new(sub_pie,"0x67")
power_sensor_09 = Ina219PowerSensor.create_new(sub_pie,"0x68")
power_sensor_10 = Ina219PowerSensor.create_new(sub_pie,"0x69")
power_sensor_11 = Ina219PowerSensor.create_new(sub_pie,"0x6a")
print("Create Ina219PowerSensor Done")
print("Start create M3HMotorcontroller")
motor_controller_01 = M3HMotorcontroller.create_new(name = "M3H 1", rasperry_pie = main_pie, address = "0x54")
motor_controller_02 = M3HMotorcontroller.create_new(name = "M3H 2", rasperry_pie = main_pie, address = "0x32")
motor_controller_05 = M3HMotorcontroller.create_new(name = "M3H an DB", rasperry_pie = db_pie, address = "0x2e")
motor_controller_06 = M3HMotorcontroller.create_new(sub_pie, name = "M3H an Sub 1", address = "0x2c")
motor_controller_07 = M3HMotorcontroller.create_new(sub_pie,"0x46","PS and Sub 2")
motor_controller_08 = M3HMotorcontroller.create_new(sub_pie,"0x6b")
motor_controller_09 = M3HMotorcontroller.create_new(sub_pie,"0x6e")
print("Create M3HMotorcontroller Done")

print("Testdata was reset")


#TODO Nächster Schritt, Motorcontroller auf RPI, PowerSensor und RELAY Basis implementieren, danach erstmal einen commit machen