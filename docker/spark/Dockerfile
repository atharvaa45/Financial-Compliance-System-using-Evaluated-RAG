FROM apache/spark

USER root

# 1. Install system tools
RUN apt-get update && \
    apt-get install -y python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
RUN pip3 install --no-cache-dir \
    pyspark \
    beautifulsoup4 \
    spacy \
    pandas \
    minio \
    boto3 \
    jupyterlab

# # 3. Download JARs for S3/MinIO support --- directly used this spark/hadoop version combo
# WORKDIR /opt/spark/jars
# RUN curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
#     curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

# # 4. Set up work directory
# WORKDIR /opt/spark/work-dir

# Switch back to default user
USER 185