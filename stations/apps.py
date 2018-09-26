from django.apps import AppConfig
from stations.models import Station, Inspection
from stations.fixtures import stations_data


class StationsConfig(AppConfig):
    name = 'stations'

    def ready(self):

        """ Initilize the list of Stations and Inspections """

        data = Inspection.objects.read_inspections()

        for station in stations_data.stations:
            station = Station(station["name"], station["location"]).save()

            if not data:
                Inspection(station, timestamp=False).save()

        if data:
            Inspection.objects.delete_all()
            for item in data:
                Inspection.to_obj(item).save()
