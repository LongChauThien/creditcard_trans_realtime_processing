from kafka import KafkaProducer
from datetime import datetime
import time
from json import dumps
import random
import pandas as pd
import os

# pip install kafka-python
# pip3 install kafka-python

from configparser import ConfigParser

# Loading Kafka Cluster/Server details from configuration file(datamaking_app.conf)
conf_file_path = "/code/kafka_producer_consumer"
conf_file_name = conf_file_path + "/creditcard_app.conf"
config_obj = ConfigParser()
config_read_obj = config_obj.read(conf_file_name)

# Kafka Cluster/Server Details
kafka_host_name = config_obj.get('kafka', 'host')
kafka_port_no = config_obj.get('kafka', 'port_no')
kafka_topic_name = config_obj.get('kafka', 'input_topic_name')

KAFKA_TOPIC_NAME_CONS = kafka_topic_name
KAFKA_BOOTSTRAP_SERVERS_CONS = kafka_host_name + ':' + kafka_port_no

if __name__ == "__main__":
    print("Kafka Producer Application Started ... ")

    # KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
    # key(topic) value(message or data record)
    kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
                                       value_serializer=lambda x: dumps(x).encode('utf-8'))

    data = pd.read_csv(conf_file_path+'/creditcard.csv')
    df = pd.DataFrame(data)

    for i in range(6290,7000):
        message = {}
        print("Preparing message: " + str(i))
        event_datetime = datetime.now()
        message['Id'] = str(event_datetime)
        message['Time'] = df['Time'][i]
        message['Amount'] = df['Amount'][i]
        for j in range(28):
            message['V'+str(j+1)] = df['V'+str(j+1)][i]
        # message['Class'] = str(df['Class'][i])
        # print("Message: ", message)
        #message_list.append(message)
        kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS, message)
        time.sleep(3)


    print("Kafka Producer Application Completed. ")