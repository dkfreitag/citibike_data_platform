import unittest
import ec2_producer


class TestProducerMethods(unittest.TestCase):
    def test_process_station_status(self):
        station_status_object = {
            "data": {
                "stations": [
                    {
                        "is_renting": 0,
                        "vehicle_types_available": [
                            {"count": 0, "vehicle_type_id": "1"},
                            {"count": 0, "vehicle_type_id": "2"},
                        ],
                        "num_bikes_available": 0,
                        "station_id": "66dbc420-0aca-11e7-82f6-3863bb44ef7c",
                        "num_bikes_disabled": 0,
                        "num_docks_disabled": 0,
                        "last_reported": 1749473240,
                        "is_returning": 0,
                        "num_docks_available": 51,
                        "is_installed": 0,
                        "num_ebikes_available": 0,
                    },
                    {
                        "is_renting": 0,
                        "vehicle_types_available": [
                            {"count": 0, "vehicle_type_id": "1"},
                            {"count": 0, "vehicle_type_id": "2"},
                        ],
                        "num_bikes_available": 0,
                        "station_id": "ffae66ec-7c16-436f-bd0a-eedf81d580e7",
                        "num_bikes_disabled": 0,
                        "num_docks_disabled": 0,
                        "last_reported": 1747399333,
                        "is_returning": 0,
                        "num_docks_available": 0,
                        "is_installed": 0,
                        "num_ebikes_available": 0,
                    },
                    {
                        "is_renting": 0,
                        "vehicle_types_available": [
                            {"count": 0, "vehicle_type_id": "1"},
                            {"count": 0, "vehicle_type_id": "2"},
                        ],
                        "num_bikes_available": 0,
                        "station_id": "66dde4ef-0aca-11e7-82f6-3863bb44ef7c",
                        "num_bikes_disabled": 0,
                        "num_docks_disabled": 0,
                        "last_reported": 1749838767,
                        "is_returning": 0,
                        "num_docks_available": 0,
                        "is_installed": 0,
                        "num_ebikes_available": 0,
                    },
                    {
                        "num_scooters_available": 0,
                        "is_renting": 1,
                        "vehicle_types_available": [
                            {"count": 3, "vehicle_type_id": "1"},
                            {"count": 8, "vehicle_type_id": "2"},
                        ],
                        "num_bikes_available": 11,
                        "station_id": "3e1bdcec-e762-4e83-b447-007f05923cce",
                        "num_bikes_disabled": 1,
                        "num_scooters_unavailable": 0,
                        "num_docks_disabled": 0,
                        "last_reported": 1749914500,
                        "is_returning": 1,
                        "num_docks_available": 11,
                        "is_installed": 1,
                        "num_ebikes_available": 8,
                    },
                ]
            },
            "last_updated": 1749914636,
            "ttl": 60,
            "version": "2.3",
        }

        station_status_records = [
            {
                "last_updated": 1749914636,
                "version": "2.3",
                "is_renting": 0,
                "station_id": "66dbc420-0aca-11e7-82f6-3863bb44ef7c",
                "num_bikes_disabled": 0,
                "num_docks_disabled": 0,
                "is_installed": 0,
                "is_returning": 0,
                "num_docks_available": 51,
                "last_reported": 1749473240,
                "num_bikes_available": 0,
                "num_ebikes_available": 0,
                "vehicle_type_id_1_count": 0,
                "vehicle_type_id_2_count": 0,
            },
            {
                "last_updated": 1749914636,
                "version": "2.3",
                "is_renting": 0,
                "station_id": "ffae66ec-7c16-436f-bd0a-eedf81d580e7",
                "num_bikes_disabled": 0,
                "num_docks_disabled": 0,
                "is_installed": 0,
                "is_returning": 0,
                "num_docks_available": 0,
                "last_reported": 1747399333,
                "num_bikes_available": 0,
                "num_ebikes_available": 0,
                "vehicle_type_id_1_count": 0,
                "vehicle_type_id_2_count": 0,
            },
            {
                "last_updated": 1749914636,
                "version": "2.3",
                "is_renting": 0,
                "station_id": "66dde4ef-0aca-11e7-82f6-3863bb44ef7c",
                "num_bikes_disabled": 0,
                "num_docks_disabled": 0,
                "is_installed": 0,
                "is_returning": 0,
                "num_docks_available": 0,
                "last_reported": 1749838767,
                "num_bikes_available": 0,
                "num_ebikes_available": 0,
                "vehicle_type_id_1_count": 0,
                "vehicle_type_id_2_count": 0,
            },
            {
                "last_updated": 1749914636,
                "version": "2.3",
                "is_renting": 1,
                "station_id": "3e1bdcec-e762-4e83-b447-007f05923cce",
                "num_bikes_disabled": 1,
                "num_docks_disabled": 0,
                "is_installed": 1,
                "is_returning": 1,
                "num_docks_available": 11,
                "last_reported": 1749914500,
                "num_bikes_available": 11,
                "num_ebikes_available": 8,
                "vehicle_type_id_1_count": 3,
                "vehicle_type_id_2_count": 8,
            },
        ]

        self.assertEqual(
            ec2_producer.process_station_status(station_status_object),
            station_status_records,
        )


if __name__ == "__main__":
    unittest.main()
