from datetime import datetime
from visual_inspection.settings import VI_FILENAME
import json
import os


class StationsManager():
    """ Manager for the weather stations """

    data = {}

    def add(self, obj):
        key = obj.name  # station name
        self.data[key] = obj
        return self.data[key]

    def all(self):
        """ Return a list of Stations objects """
        return list(self.data.values())

    def delete_all(self):
        self.data = {}
        return self.all()

    def get_by_name(self, name):
        if name in self.data.keys():
            return self.data[name]
        else:
            return None


class Station():
    """ Weather station in the observatory """

    objects = StationsManager()

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def save(self):
        res = self.objects.add(self)
        return res


class InspectionsManager():
    """ Manager for the Inspections. It saves the registries in a json file """

    inspections = {}

    def add(self, obj):
        """ It add or update an inspection with the specified station
        in the dictionary """
        self.inspections[obj.station.name] = obj
        return obj

    def all(self):
        """ Returns the dictionary of inspections """
        return list(self.inspections.values())

    def delete_all(self):
        """ Delete all the inspections """
        self.inspections = {}

    def dump_inspections(self, filename=None):
        """ It dumps the data in the dictionary in the json file """
        if not filename:
            filename = VI_FILENAME
        data = [item.to_dict() for item in self.all()]
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def read_inspections(self, filename=None):
        """ It returns the data in the json file as a list of dictionaries """
        if not filename:
            filename = VI_FILENAME
        data = []
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                data = json.load(infile)
        return data

    def load_inspections(self, inspections):
        self.delete_all()
        for inspection in inspections:
            self.add(inspection)


class Inspection():
    """ Visual inspection that confirm weather conditions in a Station """

    objects = InspectionsManager()

    def __init__(self, station, username, created_at=None, timestamp=True):
        """Constructor. It creates a registry for a specific Station"""
        self.station = station
        self.username = username
        if created_at:
            self.created_at = created_at
        else:
            datetime_min = datetime(1900, 1, 1)
            self.created_at = datetime.utcnow() if timestamp else datetime_min

    def save(self, filename=None):
        try:
            inspection = self.objects.add(self)
            if filename:
                self.objects.dump_inspections(filename=filename)
            else:
                self.objects.dump_inspections()
        except json.JSONDecodeError:
            inspection = None
        return inspection

    def to_dict(self):
        """Return a representation as a dictionary of the Inspection object"""
        formatted_timestamp = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return {"station": self.station.name,
                "username": self.username,
                "timestamp": formatted_timestamp}

    @classmethod
    def to_obj(self, obj_dict):
        """Return an Inspection object from a dictionary representation"""
        station = Station.objects.get_by_name(obj_dict["station"])
        created_at = datetime.strptime(obj_dict["timestamp"],
                                       '%Y-%m-%dT%H:%M:%S.%f')
        username = obj_dict["username"]
        return Inspection(station, username, created_at=created_at)
