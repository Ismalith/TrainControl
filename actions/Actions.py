from core.Exceptions import DBOrgaException, TrackException
from database.Database import Database
from pie_hardware.Ina219PowerSensor import Ina219PowerSensor
from pie_hardware.RasperryPie import RasperryPie


class Actions:
    @classmethod
    def create_track(cls, name = None,length_mm:int = 0, radius:int = 0, part_of_cycle:float = 0.0, slope:float = 0.0, increase_mm:int = 0, rasperry:str = None, trackgroup = None, ads1115adconverter = None, ina219powersensor = None, relay = None, motorcontroller = None, dead:bool = False):
        if not dead and (ina219powersensor is None or relay is None or motorcontroller is None):
            raise TrackException ("Error while creating track " + str(name) + ", tracks must have all components, or none and be marked as 'dead', all other configurations are illegal\n" +
                   "INA219POWERSENSOR: " + str(ina219powersensor) + "\n"
                   "RELAY: " + str(relay) + "\n"
                   "MOTORCONTROLLER: " +str(motorcontroller) + "\n"
                   "set as dead:" + str(dead))

        rasperry:RasperryPie = RasperryPie.get_for_id(rasperry)
        ina219powersensor:Ina219PowerSensor = Ina219PowerSensor.create_new("main", name="Test2", address="0x22")
        print(rasperry)
        print(ina219powersensor)

        if name is None:
            highest_generic_id_name = Database.run_sql_query("SELECT name FROM track WHERE name ~ '^Track \\d+$'ORDER BY name DESC LIMIT 1")
            id_name = int(str(highest_generic_id_name).rsplit(" ")[1]) + 1
        else:
            if trackgroup is None:
                found_tracks = Database.run_sql_query("SELECT count(track.oid) FROM track"
                    "JOIN rasperrypie rp ON track.rasperrypie = rp.oid"
                    "LEFT JOIN trackgroup tg ON track.oid = tg.track"
                    "WHERE rp.name = 'main' AND trackgroup IS NULL AND track.name = 'Track 2'")
                if found_tracks > 0:
                    raise DBOrgaException("The name " + name + " is already in use for another track with no track group on the same pie")

            else:
                found_tracks = Database.run_sql_query("SELECT count(track.oid) FROM track"
                    "JOIN rasperrypie rp ON track.rasperrypie = rp.oid"
                    "LEFT JOIN trackgroup tg ON track.oid = tg.track"
                    "WHERE rp.id = 'main' AND trackgroup = 'Gruppe 1' AND track.id = 'Track 2'")
            if found_tracks > 0:
                raise DBOrgaException("The name " + name + " is already in use for another track in the same group on the same pie")






    @classmethod
    def connect_track(cls):
        raise Exception("connect_track is not implemented")
        #TODO Implement