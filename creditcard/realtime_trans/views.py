from django.shortcuts import render
from .models import Creditcard
from django.db.models import Q
from .forms import TransactionQuery, IdQuery
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess
import os 

kafka_producer_pid = None
spark_processing_pid = None

# Create your views here.
def index(request):
    return render(request, 'index.html')


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
        
def query_ids(request):
    if request.method == 'POST':
        form = IdQuery(request.POST)
        if form.is_valid():
            transactions = Creditcard.objects.all()
            print(form.cleaned_data['class_field'])
            print(form.cleaned_data['amount'])
            print(form.cleaned_data['time'])
            if form.cleaned_data['time'] is not None:
                transactions = transactions.filter(Q(time__gte=form.cleaned_data['time']-3) & Q(time__lte=form.cleaned_data['time']+3))

            if form.cleaned_data['amount'] is not None:
                transactions = transactions.filter(Q(amount__gte=form.cleaned_data['amount']-20) & Q(amount__lte=form.cleaned_data['amount']+20))

            if form.cleaned_data['class_field'] is not None:
                transactions = transactions.filter(class_field=form.cleaned_data['class_field'])
            

            transaction_data = [
                {
                    'id': transaction.id
                }
                for transaction in transactions
            ]
            if transaction_data is None:
                transaction_data = []
            return JsonResponse({'transaction_data': transaction_data}, status=200)
        else:
            return JsonResponse({'status': 'Error', 'error': form.errors}, status=400)
        
def query_transaction(request):
    if request.method == 'POST':
        form = TransactionQuery(request.POST)
        if form.is_valid():
            try:
                transaction = Creditcard.objects.get(id=form.cleaned_data['id'])
            except Creditcard.DoesNotExist:
                transaction = None
            # print(transaction)
            if transaction is not None:
                transaction_data = {
                        'time': transaction.time,
                        'amount': transaction.amount,
                        'v1': transaction.v1,
                        'v2': transaction.v2,
                        'v3': transaction.v3,
                        'v4': transaction.v4,
                        'v5': transaction.v5,
                        'v6': transaction.v6,
                        'v7': transaction.v7,
                        'v8': transaction.v8,
                        'v9': transaction.v9,
                        'v10': transaction.v10,
                        'v11': transaction.v11,
                        'v12': transaction.v12,
                        'v13': transaction.v13,
                        'v14': transaction.v14,
                        'v15': transaction.v15,
                        'v16': transaction.v16,
                        'v17': transaction.v17,
                        'v18': transaction.v18,
                        'v19': transaction.v19,
                        'v20': transaction.v20,
                        'v21': transaction.v21,
                        'v22': transaction.v22,
                        'v23': transaction.v23,
                        'v24': transaction.v24,
                        'v25': transaction.v25,
                        'v26': transaction.v26,
                        'v27': transaction.v27,
                        'v28': transaction.v28,
                        'class_field': transaction.class_field
                    }
            else:
                transaction_data = None
            
            return JsonResponse({'transaction_data': transaction_data}, status=200)
        else:
            return JsonResponse({'status': 'Error', 'error': form.errors}, status=400)
