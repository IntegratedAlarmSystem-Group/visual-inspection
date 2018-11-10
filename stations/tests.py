from django.test import TestCase
from freezegun import freeze_time
from datetime import datetime
from stations.models import Station, Inspection
import os


class StationsTestCase(TestCase):

    def setUp(self):
        Station.objects.delete_all()

    def test_station_save(self):

        res = Station(
            'Station Test',
            'Dummy Location',
            'Primary',
            'Secondary').save()

        self.assertEqual(res.name, 'Station Test')
        self.assertEqual(res.location, 'Dummy Location')
        self.assertEqual(res.primary, 'Primary')
        self.assertEqual(res.secondary, 'Secondary')

    def test_station_should_not_be_stored_if_repeated(self):

        for i in range(2):
            Station('Station Test', 'Dummy Location','P','S').save()

        stations = Station.objects.all()

        self.assertEqual(len(stations), 1)

    def test_stations_list(self):

        # arrange
        expected_count = 10
        for i in range(expected_count):
            Station(
                'Station {}'.format(i),
                'Location {}'.format(i),
                'P',
                'S'
            ).save()

        # act
        stations = Station.objects.all()

        # assert
        self.assertTrue(isinstance(stations, list))
        self.assertEqual(len(stations), expected_count)

    def test_station_objects_references(self):

        station_1 = Station('Station 1', 'Location 1', 'P', 'S')
        station_2 = Station('Station 2', 'Location 2', 'P', 'S')

        self.assertEqual(
            id(station_1.objects),
            id(station_2.objects)
        )

        self.assertEqual(
            id(station_1.objects.data),
            id(station_2.objects.data)
        )


class InspectionTestCase(TestCase):

    def setUp(self):
        self.test_filename = "test_inspections.json"
        Inspection.objects.delete_all()
        self.station = Station("dummyStation", "Location", 'P', 'S').save()
        self.username = "usertest"

    def tearDown(self):
        if os.path.isfile(self.test_filename):
            os.remove(self.test_filename)

    def test_inspection_to_dict(self):
        # Arrange
        inspection = Inspection(self.station, self.username, timestamp=False)

        # Act
        inspection_dict = inspection.to_dict()

        # Assert
        expected_data = {"station": "dummyStation",
                         "timestamp": '1900-01-01T00:00:00.000',
                         "username": "usertest"}
        self.assertEqual(inspection_dict, expected_data)

    def test_add_inspection_with_old_timestamp(self):
        # Arrange
        datetime_min = datetime(1900, 1, 1)

        # Act
        Inspection(self.station, self.username, timestamp=False).save(
            filename=self.test_filename
        )

        # Assert
        inspections = Inspection.objects.all()
        self.assertEqual(len(inspections), 1)
        self.assertEqual(inspections[0].station, self.station)

        self.assertEqual(inspections[0].created_at, datetime_min)

    def test_add_inspection_with_current_timestamp(self):
        # Act
        timestamp = datetime(2018, 9, 25)
        with freeze_time(timestamp):
            Inspection(self.station, self.username).save(filename=self.test_filename)

        # Assert
        inspections = Inspection.objects.all()
        self.assertEqual(len(inspections), 1)
        self.assertEqual(inspections[0].station, self.station)
        self.assertEqual(inspections[0].created_at, timestamp)

    def test_dump_inspections_in_file(self):
        # Arrange
        stations = [
            Station("S{}".format(i), "Loc", 'P', 'S').save() for i in range(5)
        ]
        for station in stations:
            Inspection(station, self.username).save(
                filename=self.test_filename
            )
        self.assertEqual(len(Inspection.objects.all()), 5)

        # Act
        Inspection.objects.dump_inspections(filename=self.test_filename)

        # Assert
        expected_data = []
        for inspection in Inspection.objects.all():
            expected_data.append(inspection.to_dict())

        inspections = Inspection.objects.read_inspections(
            filename=self.test_filename
        )
        for inspection in inspections:
            self.assertTrue(inspection in expected_data)
