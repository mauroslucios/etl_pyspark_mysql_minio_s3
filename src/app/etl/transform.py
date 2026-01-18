import os
from app.utils.spark_session import get_spark
from app.config.logs.logs import get_logger
ETLLogger = get_logger()


spark = get_spark()


def transform_bronze_to_silver():
    ETLLogger.info("Transformando bronze para silver")
    bucket = os.getenv("MINIO_BUCKET")

    consulta_df = spark.read.parquet(
        f"s3a://{bucket}/bronze/consulta/"
    )

    consulta_df = (
        consulta_df
        .withColumnRenamed("data_consulta","dt_consulta")
        .withColumnRenamed("data_inicial_sintoma","dt_inicial_sintoma")
    )

    consulta_df.write.mode("overwrite").parquet(
        f"s3a://{bucket}/silver/consulta/"
    )

    ETLLogger.info("Silver consulta criada com sucesso")