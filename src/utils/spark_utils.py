from pyspark.sql import SparkSession
from utils.environment_utils import get_env_var

def build_spark_session(app_name: str):
    """
    Creates and configures a Spark session for OSS integration.
    
    Args:
        app_name (str): The name of the Spark application.
    
    Returns:
        SparkSession: Configured Spark session.
    """

    oss_endpoint = get_env_var("OSS_ENDPOINT")
    oss_access_key_id = get_env_var("OSS_ACCESS_KEY_ID")
    oss_access_key_secret = get_env_var("OSS_ACCESS_KEY_SECRET")

    return (SparkSession.builder
            .appName(app_name)
            .config("spark.hadoop.fs.oss.impl", "org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem")
            .config("spark.hadoop.fs.oss.endpoint", oss_endpoint)
            .config("spark.hadoop.fs.oss.accessKeyId", oss_access_key_id)
            .config("spark.hadoop.fs.oss.accessKeySecret", oss_access_key_secret)
            .getOrCreate())

def read_data(spark, format, input_path):
    """
    Reads data from the specified input path in OSS.
    
    Args:
        spark (SparkSession): Active Spark session.
        format (str): Data format (e.g., parquet, csv, json).
        input_path (str): Path to the input data in OSS.
    
    Returns:
        DataFrame: Loaded data.
    """
    return spark.read.format(format).load(input_path)

def write_data(df, format, save_mode, output_path):
    """
    Writes DataFrame to the specified output path in OSS.
    
    Args:
        df (DataFrame): Data to be written.
        format (str): Output format (e.g., parquet, csv, json).
        save_mode (str): Write mode (e.g., overwrite, append).
        output_path (str): Path to save the output data in OSS.
    """
    df.write.format(format).mode(save_mode).save(output_path)
