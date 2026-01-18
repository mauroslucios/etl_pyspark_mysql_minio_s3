import os
from pyspark.sql import SparkSession
from dotenv import load_dotenv

load_dotenv()


def get_spark():
    return (
        SparkSession.builder
        .appName("Analytics-ETL")
        .config("spark.sql.session.timeZone", "UTC")

        # S3A / MinIO
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("MINIO_ENDPOINT"))
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("MINIO_USER"))
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("MINIO_PASSWORD"))
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")

        # Performance / compatibilidade local
        .config("spark.hadoop.fs.s3a.fast.upload", "true")
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")

        .getOrCreate()
    )
