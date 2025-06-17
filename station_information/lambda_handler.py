import time
import json
import urllib3
import boto3

def lambda_handler(event, context):

    # initialize clients
    http = urllib3.PoolManager()
    s3 = boto3.client("s3")

    # pull data from Citibike API
    r = http.request("GET", "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json")
    station_information_object = json.loads(r.data.decode(encoding="utf-8", errors="strict"))

    # process JSON
    last_updated = station_information_object['last_updated']
    version = station_information_object['version']

    station_information_records = []

    for station in range(len(station_information_object['data']['stations'])):
        record = {}

        # metadata common to all records
        record['last_updated'] = last_updated
        record['version'] = version

        # parse each station
        record['station_id'] = station_information_object['data']['stations'][station]['station_id']
        record['lon'] = station_information_object['data']['stations'][station]['lon']
        record['lat'] = station_information_object['data']['stations'][station]['lat']
        record['short_name'] = station_information_object['data']['stations'][station]['short_name']
        if 'region_id' not in station_information_object['data']['stations'][station]:
            record['region_id'] = None
        else:
            record['region_id'] = station_information_object['data']['stations'][station]['region_id']
        record['name'] = station_information_object['data']['stations'][station]['name']
        record['capacity'] = station_information_object['data']['stations'][station]['capacity']

        station_information_records.append(record)

    # turn each station's dictionary into a single row with list comprehension
    # then, join together with newline characters to place a newline at the end of each row
    object_body = "\n".join([json.dumps(msg_obj) for msg_obj in station_information_records])

    bucket_name = "citibike-data-platform-project-bucket"
    object_key = f'station_information/station_information_lambda_output_{str(time.time())}'

    response = s3.put_object(
        Bucket=bucket_name, Key=object_key, Body=object_body
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f's3.put_object() response:\n{response}')
    }
