from datetime import datetime
from stations.fixtures import stations_data
import json


class StationsManager():
    """ Manager for the weather stations """

    data = []

    def add(self, obj):
        self.data.append(obj)

    def all(self):
        """ Return a list of Stations objects """
        return self.data

class Station():
    """ Weather station in the observatory """

    objects = StationsManager()

    def __init__(self, name, location):
        self.name = name
        self.location = location

class InspectionsManager():
    """ Manager for the Inspections. It saves the registries in a json file """

    inspections = {}
    output_filename = 'inspections.json'

    def all(self):
        """ Returns the dictionary of inspections """
        return self.inspections

    def add(self, station_name):
        """ It updates inspection object associated with the specified station
        in the dictionary and dumps the updated data in the json file.
        It returns the inspection object if it was added successfully and None
        if it was not. """
        inspection = self._add(station_name)
        if inspection:
            try:
                self.dump_inspections()
            except json.JSONDecodeError:
                inspection = None
        return inspection

    def dump_inspections(self):
        """ It dumps the data in the dictionary in the json file """
        data = []
        for station in self.inspections.keys():
            data.append(self.inspections[station].to_dict())
        with open(self.output_filename, 'w') as outfile:
            json.dump(data, outfile)

    def load_inspections(self):
        """ It returns the data in the json file as a dictionary """
        inspections = ""
        with open(self.output_filename, 'r') as outfile:
            inspections = json.load(outfile)
        return inspections

    def _validate_station(self, station_name):
        """ Return True if the station is valid and False if it is not """
        stations = self.inspections.keys()
        return True if station_name in stations else False

    def _add(self, station_name):
        """ It updates inspection object associated with the specified station
        in the dictionary """
        if self._validate_station(station_name):
            self.inspections[station_name] = Inspection(station_name)
            return self.inspections[station_name]
        else:
            return None

class Inspection():
    """ Visual inspection that confirm weather conditions in a Station """

    objects = InspectionsManager()

    def __init__(self, station, timestamp=True):
        """Constructor. It creates a registry for a specific Station"""
        self.station = station
        self.created_at = datetime.utcnow() if timestamp else datetime.min

    def to_dict(self):
        """Return a representation as a dictionary of the Inspection Object"""
        formatted_timestamp = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.')
        formatted_timestamp += str(int(self.created_at.microsecond/1000))
        return {"station": self.station,
                "timestamp": formatted_timestamp}
