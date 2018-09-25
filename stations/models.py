from django.db import models
from datetime import datetime


class Station():

    def __init__(self, name, location):
        self.name = name
        self.location = location

class Inspection():

    def __init__(self, station):
        self.created_at = datetime.utcnow()
        self.station = station
