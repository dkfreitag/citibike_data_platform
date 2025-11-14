# Citibike Data Platform

## High Level Summary:

A complete end-to-end data pipeline to fetch data from various Citibike hosted API endpoints, do both streaming and batch data processing, and make the data available in a serving layer for both analytics and data visualization.

This project is also a place for me to experiment with a variety of Data Engineering technologies. In particular, this project includes:
- Various AWS infrastructure:
  - Lambda
  - EC2
  - Glue
  - Athena
  - S3
- Kafka brokers, producers, and consumers (deployed via Docker containers to tiny EC2 instances - AWS MSK is $$$$$)
- Spark/PySpark
- Docker
- GitHub Actions
- Terraform
- Flink (coming soon)
- Iceberg (coming soon)


### Architecture Diagram:
```mermaid
---
title: Citibike Data Platform - Lambda Architecture
---
flowchart-elk LR
    A@{ shape: in-out, label: "CitiBike Station Status API" }
    B@{ shape: rect, label: "Kafka Producer"}
    C@{ shape: rect, label: "Kafka Broker"}
    D@{ shape: rect, label: "Kafka Consumer"}
    E@{ shape: cyl, label: "Raw JSON in S3"}
    F@{ shape: rect, label: "Flink (coming soon)"}
    G@{ shape: rect, label: "Stream analytics
    (coming soon)"}
    H@{ shape: rect, label: "Spark"}
    I@{ shape: in-out, label: "Citibike Station Info API"}
    J@{ shape: rect, label: "Lambda Function"}
    K@{ shape: cyl, label: "Raw JSON in S3"}
    L@{ shape: cyl, label: "Parquet in S3"}
    M@{ shape: rect, label: "Tables in Glue Data Catalog 
    (Iceberg coming soon)"}
    N@{ shape: rect, label: "Query with Athena"}
    O@{ shape: rect, label: "API endpoint - coming soon"}
    P@{ shape: rect, label: "WebApp - coming soon"}
    
    A --> B
    I --> J
    subgraph Ingestion
        B --> C
        C --> D
        J
    end

    subgraph Batch Processing
        D --> E
        E --> H
        J --> K
        K --> H
        H --> L
        L --> M
    end

    C --> F
    subgraph Stream Processing
        F --> G
    end

    subgraph Analytics Layer
        M --> N
    end

    G --> O
    subgraph Serving Layer
        M --> O
        O --> P
    end
```


---
## To Do List - in no particular order

- [ ] Automate the Spark job to run daily to combine the small Kafka files and join on the station information, then dump into a single parquet and drop in a bucket with folders for partitioning
- [ ] Terraform to deploy Lambda function
- [ ] Terraform to deploy Lambda function role and add S3FullAccess permissions
- [ ] Terraform to deploy S3 buckets
- [ ] Terraform to deploy Glue Data Catalog table metadata
- [ ] Terraform to deploy Spark Glue job
- [ ] Mock Kafka unit tests for Kafka Producer and Kafka Consumer
- [ ] Mock AWS environment for unit testing the S3 put methods in the Lambda function and Kafka Consumer
- [ ] Refresh station information every so often - it probably changes

---
## Misc. Resources

Running Airflow in Docker:
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

---

## Project Setup
1. Configure secrets in GitHub Actions
2. Configure variables in Hashicorp Cloud account

---
