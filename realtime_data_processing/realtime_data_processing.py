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
    print("Printing mysql_table_name: " + mysql_table_name)

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

    # spark.sparkContext.setLogLevel("ERROR")

    # train = spark.read.format("csv").load("C:\\Users\\Asus\\Documents\\HK6\\CS338\\creditcard\\kafka_producer_consumer\\creditcard.csv",header = 'True',inferSchema='True')
    # train = train.select('Time','Amount','Class')
    # assembler = VectorAssembler(inputCols=['Time','Amount'],outputCol="features")
    # # df_train = assembler.transform(train)
    # lgr = LogisticRegression(labelCol='Class',featuresCol='features')
    # pipeline = Pipeline( stages = [assembler,lgr, ])
    # model = pipeline.fit(train)
    model = PipelineModel.read().load("/code/pretrained_model/model")

    # Construct a streaming DataFrame that reads from test-topic
    trans_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", input_kafka_topic_name) \
        .option("startingOffsets", "latest") \
        .load()

    # print("Printing Schema of trans_df: ")
    # trans_df.printSchema()
    # key, value, topic, partition, offset, timestamp

    trans_df1 = trans_df.selectExpr("CAST(value AS STRING)")
    # trans_df1.printSchema()
    # Define a schema for the trans data
    # order_id,order_product_name,order_card_type,order_amount,order_datetime,order_country_name,order_city_name,order_ecommerce_website_name
    trans_schema = StructType() \
        .add("Id", StringType()) \
        .add("Time", FloatType()) \
        .add("Amount", FloatType()) 
        # .add("Class", StringType()) 

    # {'order_id': 1, 'order_product_name': 'Laptop', 'order_card_type': 'MasterCard',
    # 'order_amount': 38.48, 'order_datetime': '2020-10-21 10:59:10', 'order_country_name': 'Italy',
    # 'order_city_name': 'Rome', 'order_ecommerce_website_name': 'www.flipkart.com'}
    trans_df2 = trans_df1\
        .select(from_json(col("value"), trans_schema)\
        .alias("trans"))
    # trans_df2.printSchema()

    # trans_df2.printSchema()

    # trans -> ['order_id': 1, 'order_product_name': 'Laptop', ....]

    trans_df3 = trans_df2.select("trans.*")
    # print("Printing schema of trans_df3 before creating date & hour column from order_datetime ")
    # trans_df3.printSchema()
    # trans_agg_write_stream_pre = trans_df3 \
    #     .writeStream \
    #     .trigger(processingTime='10 seconds') \
    #     .outputMode("update") \
    #     .option("truncate", "false")\
    #     .format("console") \
    #     .start()
    # trans_agg_write_stream_pre_hdfs = trans_df3.writeStream \
    #     .trigger(processingTime='10 seconds') \
    #     .format("parquet") \
    #     .option("path", "/tmp/data/ecom_data/raw") \
    #     .option("checkpointLocation", "trans-agg-write-stream-pre-checkpoint") \
    #     .partitionBy("partition_date", "partition_hour") \
    #     .start()
    trans_df4 = model.transform(trans_df3)
    # trans_df4.printSchema()
    trans_df4 = trans_df4.select(['Id','Time','Amount','prediction'])  
    trans_df4 = trans_df4.withColumnRenamed("prediction","Class")  
    trans_agg_write_stream = trans_df4 \
        .writeStream \
        .trigger(processingTime='10 seconds') \
        .outputMode("update") \
        .foreachBatch(lambda current_df, epoc_id: save_to_mysql_table(current_df, epoc_id, mysql_table_name)) \
        .start()
 
    # trans_agg_write_stream = trans_df3 \
    #     .writeStream \
    #     .trigger(processingTime='10 seconds') \
    #     .outputMode("update") \
    #     .format("console") \
    #     .start()
    trans_agg_write_stream2 = trans_df4 \
        .writeStream \
        .trigger(processingTime='15 seconds') \
        .outputMode("update") \
        .foreachBatch(lambda current_df, epoc_id: print(epoc_id)) \
        .start()

    trans_agg_write_stream.awaitTermination()
    trans_agg_write_stream2.awaitTermination()

    print("Real-Time Data Processing Application Completed.")
