from django.test import TestCase
from freezegun import freeze_time
from datetime import datetime
from stations.fixtures import stations_data
from stations.models import StationsManager, InspectionsManager


class StationsManagerTestCase(TestCase):

    def setUp(self):
        self.station_manager = StationsManager()

    def test_station_manager_retrieve_all(self):
        stations = self.station_manager.all()
        self.assertEqual(len(stations), 11)
        self.assertEqual(stations[0].name, "MeteoTB1")
        self.assertEqual(stations[0].location, "AOS TB")


# class InspectionsManagerTestCase(TestCase):
#
#     def setUp(self):
#         self.inspections_manager = InspectionsManager()
#
#     def test_inspections_manager_add_item(self):
#         # Arrange
#         last_inspection = self.inspections_manager.all()["Meteo201"]
#         self.assertEqual(last_inspection.created_at, datetime.min)
#
#         # Act
#         timestamp = datetime(2018, 9, 25)
#         with freeze_time(timestamp):
#             self.inspections_manager._add("Meteo201")
#
#         # Assert
#         inspection = self.inspections_manager.all()["Meteo201"]
#         self.assertEqual(inspection.station, "Meteo201")
#         self.assertEqual(inspection.created_at, timestamp)
#
#     def test_inspections_manager_dumps_inspections(self):
#         # Arrange
#         last_inspection = self.inspections_manager.all()["Meteo201"]
#         self.assertEqual(last_inspection.created_at, datetime.min)
#
#         # Act
#         timestamp = datetime(2018, 9, 25)
#         with freeze_time(timestamp):
#             self.inspections_manager._add("Meteo201")
#         self.inspections_manager.dump_inspections()
#
#         # Assert
#         expected_data = []
#         for station in stations_data.stations:
#             if station["name"] == "Meteo201":
#                 timestamp = '2018-09-25T00:00:00.0'
#             else:
#                 timestamp = '1-01-01T00:00:00.0'
#             expected_data.append(
#                 {"station": station["name"],
#                  "timestamp": timestamp}
#             )
#         inspections = self.inspections_manager.load_inspections()
#         for inspection in inspections:
#             self.assertTrue(inspection in expected_data)
