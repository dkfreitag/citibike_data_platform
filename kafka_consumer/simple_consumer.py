import os
import time
import json
import logging

import boto3
from kafka import KafkaConsumer
from dotenv import load_dotenv

# Configure the logging system
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create a logger
logger = logging.getLogger(__name__)

load_dotenv()


def main():
    # reate an S3 client
    s3 = boto3.client("s3")
    bucket_name = "citibike-data-platform-project-bucket"

    # create Kafka consumer
    consumer = KafkaConsumer(
        "station-status",
        bootstrap_servers=f"{os.getenv('BROKER_PRIVATE_IP_ADDRESS')}:9092",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    message_batch = []
    for message in consumer:
        message_batch.append(
            {
                "topic": message.topic,
                "partition": message.partition,
                "offset": message.offset,
                "key": message.key,
                "value": message.value,
                "timestamp": message.timestamp,
                "header": message.header,
            }
        )

        # there are 2234 Citibike stations
        # this is one minute of data
        if len(message_batch) == 2234:
            try:
                # Unix timestamp with microseconds as object_key
                object_key = "kafka_output/" + str(time.time())

                # turn each message in the batch into a single row with list comprehension
                # then, join together with newline characters to place a newline at the end of each row
                object_body = "\n".join(
                    [json.dumps(msg_obj) for msg_obj in message_batch]
                )

                s3.put_object(Bucket=bucket_name, Key=object_key, Body=object_body)
                logger.info("Saved batch of records from Kafka.")

                # clear out message_batch
                message_batch = []

            except Exception as e:
                logger.error(f"Error uploading records! Exception: {e}")


if __name__ == "__main__":
    main()
