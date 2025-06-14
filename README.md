# Citibike Data Platform

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

### EC2 Setup
1. Configure secrets in GitHub Actions
2. Configure variables in Hashicorp Cloud account

---

Read from topic Kafka command (see if messages are arriving on the broker):

`bin/kafka-console-consumer.sh --topic station-status --bootstrap-server localhost:9092`
