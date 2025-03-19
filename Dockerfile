FROM ubuntu:22.04

# Set environment variable
ENV DEBIAN_FRONTEND=noninteractive

# Update package list
RUN apt-get update

# Install required packages
RUN apt-get -y install wget curl vim unzip

# Install system dependencies including build tools, GTK, OpenSSL, and OpenCV dev packages
RUN apt-get install -y \
    build-essential \
    libprotobuf-dev \
    libopenexr25 \
    libgstreamer1.0-0 \
    ffmpeg \
    libgstreamer-plugins-base1.0-0 \
    libexif-dev \
    python3-dev \
    dpkg \
    libssl-dev \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the Celantur SDK folder (with deb files, model .enc, and LICENSE)
COPY celantur_sdk /app/celantur_sdk
# Install Celantur SDK deb packages
# Use apt-get install -f to fix dependencies if necessary
RUN dpkg -i /app/celantur_sdk/debs/*.deb || (apt-get update && apt-get install -f -y && dpkg -i /app/celantur_sdk/debs/*.deb && rm -rf /app/celantur_sdk/debs)

# Copy project files: the src folder and Poetry configuration files
COPY src /app/src
COPY pyproject.toml /app/

RUN pip install poetry && poetry install --with dev

RUN cd /app/src/celantur_bindings && python3 setup.py build_ext --inplace

RUN mkdir -p /jars && \
    curl -o /jars/aliyun-sdk-oss-3.10.2.jar https://repo1.maven.org/maven2/com/aliyun/oss/aliyun-sdk-oss/3.10.2/aliyun-sdk-oss-3.10.2.jar && \
    curl -o /jars/hadoop-aliyun-3.2.0.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aliyun/3.2.0/hadoop-aliyun-3.2.0.jar
# Set Spark default configurations for OSS
ENV SPARK_OPTS "--jars /jars/aliyun-sdk-oss-3.10.2.jar,/jars/hadoop-aliyun-3.2.0.jar"
