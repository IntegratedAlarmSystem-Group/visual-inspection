from datetime import datetime
from stations.fixtures import stations_data
import json


class Station():
    """ Weather station in the observatory """

    def __init__(self, name, location):
        self.name = name
        self.location = location


class StationsManager():
    """ Manager for the weather stations """

    data = []

    def __init__(self):
        """ Constructor. It creates the list of Stations """
        for station in stations_data.stations:
            self.data.append(Station(station["name"], station["location"]))

    def all(self):
        """ Return a list of Stations objects """
        return self.data


class Inspection():
    """ Visual inspection that confirm weather conditions in a Station """

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


class InspectionsManager():
    """ Manager for the Inspections. It saves the registries in a json file """

    inspections = {}
    output_filename = 'inspections.json'

    def __init__(self, output_path=""):
        """ The optional output_path specify the folder where the json files
        with the registries will be located """
        for station in stations_data.stations:
            station_name = station["name"]
            inspection = Inspection(station_name, timestamp=False)
            self.inspections[station_name] = inspection

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
