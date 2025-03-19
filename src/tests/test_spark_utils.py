import pytest
from pyspark.sql import SparkSession
from utils.spark_utils import build_spark_session, read_data, write_data

def test_build_spark_session():
    spark = build_spark_session("Test App")
    assert isinstance(spark, SparkSession)

def test_read_write_data(tmp_path):
    spark = build_spark_session("Test App")
    data = [("Alice", 25), ("Bob", 30)]
    df = spark.createDataFrame(data, ["name", "age"])
    output_path = str(tmp_path / "output.parquet")
    write_data(df, "parquet", "overwrite", output_path)
    df_read = read_data(spark, "parquet", output_path)
    assert df_read.count() == 2
