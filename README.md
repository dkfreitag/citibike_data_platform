# Citibike Data Platform

Kafka Producer
Kafka Broker
Kafka Consumer

Path A:
S3
Spark batch processing

Path B:
Flink stream processing

---

### EC2 Setup
1. Create VPC - put broker and producer EC2's on the same VPC
1. Create broker EC2
2. Create producer EC2
3. Set up secrets in GitHub so CI/CD can SSH into the EC2's

---

Read from topic Kafka command (see if messages are arriving on the broker):

`bin/kafka-console-consumer.sh --topic station-status --bootstrap-server localhost:9092`
