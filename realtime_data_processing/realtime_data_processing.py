from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

from pyspark.ml import PipelineModel



import time

from configparser import ConfigParser

# Loading Kafka Cluster/Server details from configuration file(datamaking_app.conf)

conf_file_path = "/code/realtime_data_processing"
conf_file_name = conf_file_path + "/creditcard_app.conf"
config_obj = ConfigParser()
print(config_obj)
print(config_obj.sections())
config_read_obj = config_obj.read(conf_file_name)
print(type(config_read_obj))
print(config_read_obj)
print(config_obj.sections())

# Kafka Cluster/Server Details
kafka_host_name = config_obj.get('kafka', 'host')
kafka_port_no = config_obj.get('kafka', 'port_no')
input_kafka_topic_name = config_obj.get('kafka', 'input_topic_name')
output_kafka_topic_name = config_obj.get('kafka', 'output_topic_name')
kafka_bootstrap_servers = kafka_host_name + ':' + kafka_port_no

# MySQL Database Server Details
mysql_host_name = os.getenv('DATABASE_HOST','db')
mysql_port_no = os.getenv('DATABASE_PORT','3306')
mysql_user_name = os.getenv('DATABASE_USER','admin')
mysql_password = os.getenv('DATABASE_PASSWORD','123456')
mysql_database_name = os.getenv('DATABASE_NAME', 'creditcard')
mysql_driver = config_obj.get('mysql', 'driver')

mysql_table_name = config_obj.get('mysql', 'mysql_tbl')

mysql_jdbc_url = "jdbc:mysql://" + mysql_host_name + ":" + mysql_port_no + "/" + mysql_database_name
# https://mvnrepository.com/artifact/mysql/mysql-connector-java
# --packages mysql:mysql-connector-java:5.1.49

# spark-submit --master local[*] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,mysql:mysql-connector-java:5.1.49 --files /home/datamaking/workarea/code/course_download/ecom-real-time-case-study/realtime_data_processing/datamaking_app.conf /home/datamaking/workarea/code/course_download/ecom-real-time-case-study/realtime_data_processing/realtime_data_processing.py

#Create the Database properties
db_properties = {}
db_properties['user'] = mysql_user_name
db_properties['password'] = mysql_password
db_properties['driver'] = mysql_driver


def save_to_mysql_table(current_df, epoc_id, mysql_table_name):
    print("Inside save_to_mysql_table function")
    print("Printing epoc_id: ")
    print(epoc_id)
    # print("Printing mysql_table_name: " + mysql_table_name)

    mysql_jdbc_url = "jdbc:mysql://" + mysql_host_name + ":" + str(mysql_port_no) + "/" + mysql_database_name

    # current_df = current_df.withColumn('batch_no', lit(epoc_id))

    #Save the dataframe to the table.
    current_df.write.jdbc(url = mysql_jdbc_url,
                  table = mysql_table_name,
                  mode = 'append',
                  properties = db_properties)

    print("Exit out of save_to_mysql_table function")

if __name__ == "__main__":
    print("Welcome to DataMaking !!!")
    print("Real-Time Data Processing Application Started ...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

    spark = SparkSession \
        .builder \
        .appName("Real-Time Data Processing with Kafka Source and Message Format as JSON") \
        .master("local[*]") \
        .getOrCreate()


    model = PipelineModel.read().load("/code/pretrained_model/model")

    # Construct a streaming DataFrame that reads from test-topic
    trans_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", input_kafka_topic_name) \
        .option("startingOffsets", "latest") \
        .load()

    trans_df1 = trans_df.selectExpr("CAST(value AS STRING)")
    
    trans_schema = StructType() \
        .add("Id", StringType()) \
        .add("Time", FloatType()) \
        .add("Amount", FloatType()) \
        .add("V1", FloatType()) \
        .add("V2", FloatType()) \
        .add("V3", FloatType()) \
        .add("V4", FloatType()) \
        .add("V5", FloatType()) \
        .add("V6", FloatType()) \
        .add("V7", FloatType()) \
        .add("V8", FloatType()) \
        .add("V9", FloatType()) \
        .add("V10", FloatType()) \
        .add("V11", FloatType()) \
        .add("V12", FloatType()) \
        .add("V13", FloatType()) \
        .add("V14", FloatType()) \
        .add("V15", FloatType()) \
        .add("V16", FloatType()) \
        .add("V17", FloatType()) \
        .add("V18", FloatType()) \
        .add("V19", FloatType()) \
        .add("V20", FloatType()) \
        .add("V21", FloatType()) \
        .add("V22", FloatType()) \
        .add("V23", FloatType()) \
        .add("V24", FloatType()) \
        .add("V25", FloatType()) \
        .add("V26", FloatType()) \
        .add("V27", FloatType()) \
        .add("V28", FloatType()) 
    
    trans_df2 = trans_df1\
        .select(from_json(col("value"), trans_schema)\
        .alias("trans"))

    trans_df3 = trans_df2.select("trans.*")
  
    trans_df4 = model.transform(trans_df3)
    trans_df4 = trans_df4.select(['Id','Time','Amount','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28','prediction'])  
    trans_df4 = trans_df4.withColumnRenamed("prediction","Class")  
    trans_agg_write_stream = trans_df4 \
        .writeStream \
        .trigger(processingTime='3 seconds') \
        .outputMode("update") \
        .foreachBatch(lambda current_df, epoc_id: save_to_mysql_table(current_df, epoc_id, mysql_table_name)) \
        .start()

    trans_agg_write_stream.awaitTermination()

    print("Real-Time Data Processing Application Completed.")
