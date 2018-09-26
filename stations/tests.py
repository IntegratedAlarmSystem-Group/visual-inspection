from django.test import TestCase
from freezegun import freeze_time
from datetime import datetime
from stations.models import Station, Inspection
from stations.models import StationsManager, InspectionsManager
from stations.models import Station


class StationsTestCase(TestCase):

    def setUp(self):
        Station.objects.delete_all()

    def test_station_save(self):

        res = Station('Station Test', 'Dummy Location').save()

        self.assertEqual(res.name, 'Station Test')
        self.assertEqual(res.location, 'Dummy Location')

    def test_station_should_not_be_stored_if_repeated(self):

        for i in range(2):
            Station('Station Test', 'Dummy Location').save()

        stations = Station.objects.all()

        self.assertEqual(len(stations), 1)


    def test_stations_list(self):

        # arrange
        expected_count = 10
        for i in range(expected_count):
            Station(
                'Station {}'.format(i),
                'Location {}'.format(i)
            ).save()

        # act
        stations = Station.objects.all()

        # assert
        self.assertTrue(isinstance(stations, list))
        self.assertEqual(len(stations), expected_count)

    def test_station_objects_reference(self):

        station_1 = Station('Station 1', 'Location 1')
        station_2 = Station('Station 2', 'Location 2')

        self.assertEqual(
            id(station_1.objects), id(station_2.objects)
        )

class InspectionTestCase(TestCase):

    def setUp(self):
        Inspection.objects.delete_all()
        self.station = Station("dummyStation", "Location dummy").save()

    def test_inspection_to_dict(self):
        # Arrange
        inspection = Inspection(self.station, timestamp=False)

        # Act
        inspection_dict = inspection.to_dict()

        # Assert
        expected_data = {"station": "dummyStation",
                         "timestamp": '1-01-01T00:00:00.0'}
        self.assertEqual(inspection_dict, expected_data)

    def test_add_inspection_with_old_timestamp(self):
        # Act
        Inspection(self.station, timestamp=False).save()

        # Assert
        inspections = Inspection.objects.all()
        self.assertEqual(len(inspections), 1)
        self.assertEqual(inspections[0].station, self.station)
        self.assertEqual(inspections[0].timestamp, datetime.min)

    def test_add_inspection_with_current_timestamp(self):
        # Act
        timestamp = datetime(2018, 9, 25)
        with freeze_time(timestamp):
            Inspection(self.station).save()

        # Assert
        inspections = Inspection.objects.all()
        self.assertEqual(len(inspections), 1)
        self.assertEqual(inspections[0].station, self.station)
        self.assertEqual(inspections[0].timestamp, timestamp)

    def test_dump_inspections_in_file(self):
        # Arrange
        stations = [Station("S{}".format(i), "Loc").save() for i in range(5)]
        for station in stations:
            Inspection(station).save()
        self.assertEqual(len(Inspection.objects.all(), 5))

        # Act
        Inspection.objects.dump_inspections()

        # Assert
        expected_data = []
        for inspection in Inspection.objects.all():
            expected_data.append(inspection.to_dict())

        inspections = self.inspections_manager.load_inspections()
        for inspection in inspections:
            self.assertTrue(inspection in expected_data)


# class InspectionsManagerTestCase(TestCase):
#
#     def setUp(self):
#         self.inspections_manager = InspectionsManager()
#
#     def test_inspections_manager_add_item(self):
#         # Arrange
#         last_inspection = self.inspections_manager.all()["Meteo201"]
#         self.assertEqual(last_inspection.created_at, datetime.min)

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
