from django.apps import AppConfig
from stations.models import Station, Inspection
from stations.fixtures import stations_data


class StationsConfig(AppConfig):
    name = 'stations'

    def ready(self):

        """ Initilize the list of Stations and Inspections """

        for station in stations_data.stations:
            station = Station(station["name"], station["location"]).save()
            inspection = Inspection(station, timestamp=False).save()
