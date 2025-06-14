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
1. Create VPC - put broker and producer EC2's on the same VPC
1. Create broker EC2
2. Create producer EC2
3. Set up secrets in GitHub so CI/CD can SSH into the EC2's

---

Read from topic Kafka command (see if messages are arriving on the broker):

`bin/kafka-console-consumer.sh --topic station-status --bootstrap-server localhost:9092`
