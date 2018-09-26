from datetime import datetime
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

    def add(self, obj):
        """ It add or update an inspection with the specified station
        in the dictionary """
        self.inspections[obj.name] = obj
        return obj

    def all(self):
        """ Returns the dictionary of inspections """
        return self.inspections.values()

    def delete_all(self):
        """ Delete all the inspections """
        self.inspections = {}

    def dump_inspections(self):
        """ It dumps the data in the dictionary in the json file """
        data = [item.to_dict() for item in self.inspections.values()]
        with open(self.output_filename, 'w') as outfile:
            json.dump(data, outfile)

    def load_inspections(self):
        """ It returns the data in the json file as a list of dictionaries """
        data = []
        with open(self.output_filename, 'r') as outfile:
            data = json.load(outfile)
        return data

    # def validate_station(self, obj):
    #     """ Return True if the station is valid and False if it is not """
    #     stations_names = [station["name"] for station in stations]
    #     return True if obj.name in stations_names else False


class Inspection():
    """ Visual inspection that confirm weather conditions in a Station """

    objects = InspectionsManager()

    def __init__(self, station, timestamp=True):
        """Constructor. It creates a registry for a specific Station"""
        self.station = station
        self.created_at = datetime.utcnow() if timestamp else datetime.min

    def save(self):
        try:
            inspection = self.objects.add(self)
            self.objects.dump_inspections(self)
        except json.JSONDecodeError:
            inspection = None
        return inspection

    def to_dict(self):
        """Return a representation as a dictionary of the Inspection Object"""
        formatted_timestamp = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.')
        formatted_timestamp += str(int(self.created_at.microsecond/1000))
        return {"station": self.station.name,
                "timestamp": formatted_timestamp}
