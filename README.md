# Citibike Data Platform

---
## To Do:

Update to use ECR:
- [ ] Deploy Docker container to ECR
- [ ] Run Docker Compose from container in ECR
- [ ] Update Producer and Consumer to use ECR

Save records to S3:
- [ ] Use Spark to read from Kafka and write to S3

```
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaToS3Streaming") \
    .getOrCreate()

# Read from Kafka
kafka_stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "<kafka_bootstrap_servers>") \
    .option("subscribe", "<kafka_topic_name>") \
    .option("startingOffsets", "earliest") \
    .load()

# (Optional) Process and transform the data
# Example: Adding a new column
processed_df = kafka_stream_df.withColumn("processed_time", current_timestamp()) 

# Write to S3
query = processed_df.writeStream \
    .format("parquet") \
    .option("path", "s3a://<s3_bucket_name>/<s3_output_path>") \
    .option("checkpointLocation", "s3a://<s3_bucket_name>/checkpoint/") \
    .trigger(processingTime="1 minute") \  # Or trigger(availableNow=True) for periodic processing
    .start()

# Wait for the termination of the query
query.awaitTermination()
```

## Nice to have list:

- [ ] Mock Kafka unit tests for Kafka Producer

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
