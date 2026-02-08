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

# rename columns
station_status_df_renamed = station_status_df.withColumnRenamed("last_updated", "last_updated_station_status") \
                                             .withColumnRenamed("version", "version_station_status")
station_information_df_renamed = station_information_df.withColumnRenamed("last_updated", "last_updated_station_information") \
                                                       .withColumnRenamed("version", "version_station_information") \
                                                       .withColumnRenamed("station_id", "station_id_station_information") \
                                                       
full_station_df = station_status_df_renamed.join(broadcast(station_information_df_renamed), station_information_df_renamed.station_id_station_information == station_status_df_renamed.station_id)

# drop join column since we already have it
write_df = full_station_df.drop('station_id_station_information')

# Write as Parquet to S3
write_df.write.mode('overwrite').parquet('s3://citibike-data-platform-project-bucket/silver_layer/')

job.commit()
