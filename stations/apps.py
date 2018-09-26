from django.apps import AppConfig
from stations.models import Station, Inspection
from stations.fixtures import stations_data


class StationsConfig(AppConfig):
    name = 'stations'

    def ready(self):

        """ Constructor. It creates the list of Stations """

        for station in stations_data.stations:
            Station.objects.add(
                Station(station["name"], station["location"]))

        # for station in stations_data.stations:
        #     station_name = station["name"]
        #     inspection = Inspection(station_name, timestamp=False)
        #     self.inspections[station_name] = inspection
