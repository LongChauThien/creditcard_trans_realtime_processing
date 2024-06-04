from django.shortcuts import render
from .models import Creditcard
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess
import os 

kafka_producer_pid = None
spark_processing_pid = None

# Create your views here.
def index(request):
    transactions = Creditcard.objects.all()
    context = {
        'transactions': transactions
    }
    return render(request, 'index.html', context)


@csrf_exempt
def run_kafka_producer(request):
    global kafka_producer_pid
    if request.method == 'POST':
        try:
            kafka_script_path = '/code/kafka_producer_consumer/kafka_producer.py'
            process = subprocess.Popen(['python', kafka_script_path])
            kafka_producer_pid = process.pid
            return JsonResponse({'status': 'Kafka producer started','pid': kafka_producer_pid}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)

@csrf_exempt
def run_spark_processing(request):
    global spark_processing_pid
    if request.method == 'POST':
        try:
            spark_submit_cmd = ['/opt/spark/bin/spark-submit', 
                                "--master", 
                                "local[*]", 
                                "--packages", 
                                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,mysql:mysql-connector-java:8.0.33", 
                                "--files", "/code/realtime_data_processing/creditcard_app.conf", 
                                "/code/realtime_data_processing/realtime_data_processing.py"]
            process = subprocess.Popen(spark_submit_cmd)
            spark_processing_pid = process.pid
            return JsonResponse({'status': 'Spark processing started','pid': spark_processing_pid}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
        
@csrf_exempt
def stop_kafka_producer(request):
    global kafka_producer_pid
    if request.method == 'POST':
        try:
            if kafka_producer_pid:
                os.kill(kafka_producer_pid, 9)  # SIGKILL
                kafka_producer_pid = None
                return JsonResponse({'status': 'Kafka producer stopped'}, status=200)
            else:
                return JsonResponse({'status': 'No Kafka producer running'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)

@csrf_exempt
def stop_spark_processing(request):
    global spark_processing_pid
    if request.method == 'POST':
        try:
            if spark_processing_pid:
                os.kill(spark_processing_pid, 9)  # SIGKILL
                spark_processing_pid = None
                return JsonResponse({'status': 'Spark processing stopped'}, status=200)
            else:
                return JsonResponse({'status': 'No Spark processing running'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)