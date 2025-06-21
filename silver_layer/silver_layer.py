import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import broadcast

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read JSON files from S3
station_status_df = spark.read.json('s3://citibike-data-platform-project-bucket/kafka_output/*')
station_information_df = spark.read.json('s3://citibike-data-platform-project-bucket/station_information/*')

full_station_df = station_status_df.join(broadcast(station_information_df), station_status_df.station_id == station_status_df.station_id)

# Write as Parquet to S3
full_station_df.write.mode('overwrite').parquet('s3://citibike-data-platform-project-bucket/silver_layer/')

job.commit()
