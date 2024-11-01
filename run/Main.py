from Startup import Startup
from Run import Run
from Shutdown import Shutdown

if Startup.startup_db_check():
    if Startup.startup_hardware_check():
        if Startup.start():
            running = True
            while running:
                running =Run.run()

            if Shutdown.stop_all():
                if Shutdown.shutdown():
                    print("TrainControl successfully shut down, hardware can now be turned off")
