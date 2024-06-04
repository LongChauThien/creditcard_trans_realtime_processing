from django.urls import path
from .views import index, run_kafka_producer, run_spark_processing, stop_kafka_producer, stop_spark_processing

urlpatterns = [
    path('', index),
    path('run_kafka_producer/', run_kafka_producer, name='run_kafka_producer'),
    path('run_spark_processing/', run_spark_processing, name='run_spark_processing'),
    path('stop_kafka_producer/', stop_kafka_producer, name='stop_kafka_producer'),
    path('stop_spark_processing/', stop_spark_processing, name='stop_spark_processing')
]