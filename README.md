# Citibike Data Platform

---
## To Do:

- [ ] Add Kafka metadata (timestamp, partition?) to each row getting dumped into S3. Add all the timestamps you can.
- [ ] Sliver layer: Spark job to run hourly (daily)? to combine the small Kafka files and join on the station information, then dump into a single parquet and drop in a bucket with folders for partitioning. Or, can partitions just be baked into the parquet file itself?
- [ ] Terraform to deploy Lambda function
- [ ] Terraform to deploy Lambda function role and add S3FullAccess permissions
- [ ] Terraform to deploy Glue Crawlers
- [ ] Terraform to deploy S3 bucket
- [ ] Any other infra that I am forgetting?

Next:
- [ ] Get a bunch of records
- [ ] Write a Spark job to join station_information and kafka_output and save it from the raw JSON in Parquet format with partitioning and as an Iceberg table

## Misc. to do list:

- [ ] Mock Kafka unit tests for Kafka Producer and Kafka Consumer
- [ ] Mock AWS environment for unit testing the S3 put methods in the Lambda function and Kafka Consumer
- [ ] Refresh station information every so often - it probably changes
- [ ] Kafka Consumer: is there a better strategy than batches of 2234 records?

---

```
The KafkaConsumer in kafka-python does not directly "return" a value in the traditional sense of a function returning a single result. Instead, it acts as an iterable, allowing you to consume messages in a loop. 

When you iterate over a KafkaConsumer instance, such as in a for loop: 

from kafka import KafkaConsumer

consumer = KafkaConsumer('my_topic')
for msg in consumer:
    print(msg)

Each iteration of the loop yields a ConsumerRecord object. This ConsumerRecord is a namedtuple that encapsulates various attributes of the consumed message, including: 
topic: The name of the Kafka topic the message belongs to. 
partition: The partition within the topic the message was consumed from. 
offset: The offset of the message within its partition. 
key: The message key (if present). 
value: The message value. 
timestamp: The timestamp of the message. 
timestamp_type: The type of timestamp (e.g., CREATE_TIME, LOG_APPEND_TIME). 
headers: Any message headers (if present). 
In essence, the KafkaConsumer provides a continuous stream of ConsumerRecord objects as you consume messages from Kafka. 
```

---

Running Airflow in Docker:
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

---
## Project Outline:

### Data Ingestion:
Kafka Producer<br>
Kafka Broker<br>
Kafka Consumer

### Lambda Architecture

#### Batch pipeline:
S3<br>
Spark batch processing<br>
Iceberg data lake

#### Streaming pipeline:
Flink stream processing

### Serving Layer

API endpoint - queries data<br>
Display stream processing stats<br>
Display batch processing stats

---

## Project Setup
1. Configure secrets in GitHub Actions
2. Configure variables in Hashicorp Cloud account

---
