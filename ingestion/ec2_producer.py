# pip install kafka_python
from kafka import KafkaProducer

import json
import urllib3
from datetime import datetime
from datetime import timezone
import time

def fetch_station_status():
    http = urllib3.PoolManager()

    r = http.request("GET", "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json")
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))

    return r_dict

def process_station_status(station_status_object):

    lambda_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    last_updated = station_status_object['last_updated']
    version = station_status_object['version']

    station_status_records = []

    for station in range(len(station_status_object['data']['stations'])):
        record = {}

        # metadata common to all records
        record['lambda_timestamp'] = lambda_timestamp
        record['last_updated'] = last_updated
        record['version'] = version

        # parse each station
        record['is_renting'] = station_status_object['data']['stations'][station]['is_renting']
        record['station_id'] = station_status_object['data']['stations'][station]['station_id']
        record['num_bikes_disabled'] = station_status_object['data']['stations'][station]['num_bikes_disabled']
        record['num_docks_disabled'] = station_status_object['data']['stations'][station]['num_docks_disabled']
        record['is_installed'] = station_status_object['data']['stations'][station]['is_installed']
        record['is_returning'] = station_status_object['data']['stations'][station]['is_returning']
        record['num_docks_available'] = station_status_object['data']['stations'][station]['num_docks_available']
        record['last_reported'] = station_status_object['data']['stations'][station]['last_reported']
        record['num_bikes_available'] = station_status_object['data']['stations'][station]['num_bikes_available']
        record['num_ebikes_available'] = station_status_object['data']['stations'][station]['num_ebikes_available']

        # parse bike types
        for vtype in range(len(station_status_object['data']['stations'][station]['vehicle_types_available'])):
            veh_type_id = station_status_object['data']['stations'][station]['vehicle_types_available'][vtype]['vehicle_type_id']

            if veh_type_id == '1':
                record['vehicle_type_id_1_count'] = station_status_object['data']['stations'][station]['vehicle_types_available'][vtype]['count']
            elif veh_type_id == '2':
                record['vehicle_type_id_2_count'] = station_status_object['data']['stations'][station]['vehicle_types_available'][vtype]['count']
            else:
                raise Exception('Error! Unexpected vehicle type ID encountered.')

        station_status_records.append(record)

    return station_status_records


def connect_to_producer():
    # Put EC2 running Kafka on the same VPC as the Lambda function
    # BROKERS = '<internal_ip_of_ec2_running_kafka>:9092'
    BROKERS = f"10.0.3.157:9092"

    producer = KafkaProducer(
        bootstrap_servers=BROKERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        retry_backoff_ms=10,
        request_timeout_ms=30000,)

    return producer

def main():

    station_status_object = fetch_station_status()
    station_status_records = process_station_status(station_status_object)

    producer = connect_to_producer()
    topicname = 'station-status'

    for record in station_status_records:
        try:
            future = producer.send(topicname, value=record)
            producer.flush()
            print(future.get(timeout=10))

        except Exception as e:
            print(e.with_traceback())

if __name__ == '__main__':
    while True:
        main()
        time.sleep(10)
