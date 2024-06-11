#!/bin/bash

# Function to handle shutdown
shutdown() {
    echo "Shutting down Kafka..."
    $KAFKA_HOME/bin/kafka-server-stop.sh
    echo "Shutting down ZooKeeper..."
    $KAFKA_HOME/bin/zookeeper-server-stop.sh
    exit 0
}

# Trap signals to trigger the shutdown function
trap shutdown SIGTERM SIGINT

# Clean up previous ZooKeeper data
rm -rf /tmp/zookeeper/*
rm -rf /tmp/kafka-logs/*

# Start ZooKeeper
echo "Starting ZooKeeper..."
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &

# Give ZooKeeper time to start
sleep 15

# Start Kafka
echo "Starting Kafka..."
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &

sleep 15

cd /code/creditcard
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Export the DJANGO_SETTINGS_MODULE variable
# export DJANGO_SETTINGS_MODULE=creditcard.settings

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &
# daphne -b 0.0.0.0 -p 8000 creditcard.asgi:application
# Wait for all background processes to finish
wait
