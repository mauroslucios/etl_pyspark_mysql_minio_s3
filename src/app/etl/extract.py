import pandas as pd
import mysql.connector
import os
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime

from app.utils.s3 import get_s3_client
from app.config.logs.logs import get_logger

ETLLogger = get_logger()

load_dotenv()

TABLES = [
    "paciente",
    "medico",
    "consulta",
    "doenca",
    "medicamento",
    "receita",
    "receita_medicamento",
]


def extract_mysql_to_bronze():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=os.getenv("MYSQL_PORT"),
    )

    s3 = get_s3_client()
    bucket_name = os.getenv("MINIO_BUCKET")

    try:
        # Verifica se o bucket existe
        try:
            s3.head_bucket(Bucket=bucket_name)
        except Exception:
            ETLLogger.info(f"Bucket {bucket_name} não existe. Criando bucket.")
            s3.create_bucket(Bucket=bucket_name)

        for table in TABLES:
            ETLLogger.info(f"Extracting {table} from MySQL to S3")

            df = pd.read_sql(f"SELECT * FROM {table}", conn)

            buffer = BytesIO()
            df.to_parquet(buffer, index=False)
            buffer.seek(0)

            date_str = datetime.now().strftime("%Y-%m-%d")
            key = f"bronze/{table}/dt={date_str}/{table}.parquet"

            s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=buffer.getvalue(),
            )

            ETLLogger.info(
                f"Table {table} written to s3://{bucket_name}/{key}"
            )

    except Exception as e:
        ETLLogger.error(
            f"Error extracting from MySQL to S3\n{e}",
            exc_info=True
        )
        raise

    finally:
        conn.close()
        ETLLogger.info("MySQL connection closed")

    ETLLogger.info("MySQL to S3 extraction completed")