import time

#from Ads1115ADConverter import Ads1115ADConverter
#from Ina219PowerSensor import Ina219PowerSensor
from pie_hardware.Relay import Relay
from TrackGroup import TrackGroup

#from M3HMotorcontroller import M3HMotorcontroller

#ads = Ads1115ADConverter(0X48, {2, 1, 1, 0})
#ina = Ina219PowerSensor(0X40)

#i = 0
#while i <= 26:
    #if i == 2 or i == 3:
        #i = 4

    #print(i)
    #relay = Relay(i)
    #relay.close()
    #time.sleep(1)
    #relay.open()
    #i = i + 1
    #relay.shutdown()

#relay.shutdown
#track1 = M3HMotorcontroller(0x0a)
#track1.reset()

#track1.run_forward(3, 500, 5, 10, 180)
#i = 20
#while i > 0:
    #time.sleep(0.5)
    #print(track1.read_speed(3))
    #i = i - 1

#track1.run_forward(3, 0, 5, 10)
#while track1.run_reset_direction(3):
    #time.sleep(0.5)
    #print(track1.read_speed(3))
    #i = i - 1
run = 0
active_Relay = -1
while run == 1:
    command = input()
    if command == 'exit':
        if active_Relay != -1:
            Relay(active_Relay).open()
            Relay(active_Relay).shutdown()
            print('relais test finished, relay ' + str(active_Relay) + ' opend')
        run = 0
        print('relais test finished')

    elif command.isdigit() & (int(command) <= 24):
        if active_Relay != -1:
            Relay(active_Relay).open()
            Relay(active_Relay).shutdown()
        old_relay = active_Relay
        active_Relay = int(command)
        Relay(active_Relay).close()
        print('Relays ' + str(old_relay) + ' open, Relay ' + str(active_Relay) + ' closed')

trackgroup = TrackGroup(0x20,1, 2, 3)
trackgroup2 = TrackGroup(0x21,1, 2, 3)
run = 1
speed = 0
relay = Relay(4)
relay.close()
trackgroup.reset()
trackgroup2.reset()
while run == 1:
    command = input()
    if command == 'e':
        run = 0
    elif command.isdigit():
        speed = int(command)
    trackgroup.run(speed)
    trackgroup2.run(speed)
    time.sleep(1)

trackgroup.run(0)
trackgroup.run(0)

time.sleep(10)
relay.open()
relay.shutdown()
trackgroup.shutdown()
trackgroup2.shutdown()
#relay = Relay(12)
#relay.open()
#relay.close()
#relay.shutdown()