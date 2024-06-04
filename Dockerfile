# Use the official Python image as a base image
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    default-libmysqlclient-dev \
    default-jre \
    pkg-config \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Spark and Kafka tarballs
COPY spark-3.5.1-bin-hadoop3.tgz /tmp/
COPY kafka_2.13-3.6.2.tgz /tmp/

# Extract Spark
RUN tar -xzvf /tmp/spark-3.5.1-bin-hadoop3.tgz -C /opt/ && \
    mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark

# Extract Kafka
RUN tar -xzvf /tmp/kafka_2.13-3.6.2.tgz -C /opt/ && \
    mv /opt/kafka_2.13-3.6.2 /opt/kafka

# Download MySQL Connector/J
ENV MYSQL_CONNECTOR_VERSION=8.0.33
RUN curl -fsSL -o /opt/spark/jars/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar \
    https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_CONNECTOR_VERSION}/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$SPARK_HOME/bin:$KAFKA_HOME/bin:$PATH

# Set the working directory for Django
WORKDIR /code

# Copy the Django project files
COPY creditcard /code/creditcard
COPY kafka_producer_consumer /code/kafka_producer_consumer 
COPY pretrained_model /code/pretrained_model
COPY realtime_data_processing /code/realtime_data_processing
COPY entrypoint.sh requirements.txt /code/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose necessary ports for Django and Spark
EXPOSE 8000 4040 7077


COPY .ivy2/cache /root/.ivy2/cache
COPY .ivy2/jars /root/.ivy2/jars

# Command to run both Django and Spark
CMD ["bash", "-c", "/code/entrypoint.sh"]
