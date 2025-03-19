import os
import json
import oss2
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Import your Celantur Python bindings
from celentaur_bindings import CelanturProcessor

from utils.arguments_parser import parse_arguments
from utils.environment_utils import get_env_var
from utils.spark_utils import build_spark_session, read_data, write_data

def anonymize_image_and_save(image_name: str,
                             bucket_name: str,
                             model_path: str,
                             license_path: str) -> str:
    """
    Downloads an image from OSS using oss2, anonymizes it with Celantur,
    uploads the anonymized image and its detections JSON back to OSS,
    and returns a JSON string summarizing the results.
    """
    try:
        # Get OSS credentials and endpoint from environment variables
        oss_endpoint = get_env_var("OSS_ENDPOINT")
        oss_access_key_id = get_env_var("OSS_ACCESS_KEY_ID")
        oss_access_key_secret = get_env_var("OSS_ACCESS_KEY_SECRET")

        # Initialize OSS auth and create a bucket instance (bucket_name comes from the CSV)
        auth = oss2.Auth(oss_access_key_id, oss_access_key_secret)
        bucket = oss2.Bucket(auth, oss_endpoint, bucket_name)

        # Download the image from OSS
        image_bytes = bucket.get_object(image_name).read()

        # Initialize the Celantur processor and load the inference model
        processor = CelanturProcessor(license_path)
        processor.load_inference_model(model_path)

        # Process the image using Celantur
        processor.process_image(image_bytes)
        anonymized_bytes = processor.get_result()

        # Call get_detections to clear detections (or retrieve them if desired)
        processor.get_detections()

        # Construct anonymized file names:
        base, ext = os.path.splitext(image_name)
        anonymized_image_name = f"{base}_anonymized{ext}"
        detections_json_name = f"{base}_anonymized.json"

        # Upload the anonymized image back to OSS
        put_image_result = bucket.put_object(anonymized_image_name, anonymized_bytes)
        if put_image_result.status not in [200, 201]:
            raise Exception(f"Failed to upload anonymized image: {anonymized_image_name}")

        # For demonstration, we create an empty detections JSON.
        # Modify this if your SDK returns actual detections data.
        detections_data = {"detections": []}
        detections_json = json.dumps(detections_data, indent=2).encode("utf-8")

        # Upload the JSON file with detections
        put_json_result = bucket.put_object(detections_json_name, detections_json)
        if put_json_result.status not in [200, 201]:
            raise Exception(f"Failed to upload detections JSON: {detections_json_name}")

        # Build result info
        result = {
            "status": "success",
            "original_image": f"oss://{bucket_name}/{image_name}",
            "anonymized_image": f"oss://{bucket_name}/{anonymized_image_name}",
            "detections_json": f"oss://{bucket_name}/{detections_json_name}"
        }
        return json.dumps(result)

    except Exception as e:
        return json.dumps({"status": "failed", "reason": str(e)})


def main():
    # Parse command-line arguments using your utility function
    args = parse_arguments()
    input_path = args.input       # OSS path to input CSV
    output_path = args.output     # OSS path for output data
    data_format = args.format     # Expected format (e.g., csv)
    save_mode = args.save_mode    # e.g., "overwrite"

    # Retrieve Celantur model and license file paths from environment variables
    model_path = get_env_var("CELENTUR_MODEL_PATH")       # e.g., /app/celantaur_sdk/your_model.onnx.enc
    license_path = get_env_var("CELENTUR_LICENSE_PATH")     # e.g., /app/celantaur_sdk/license

    # Build a Spark session with OSS integration
    spark = build_spark_session(app_name="CelanturAnonymization")

    # Read input CSV (with headers) from OSS
    df = read_data(spark, data_format, input_path)

    # Define a UDF to call our anonymization function.
    # Assuming the CSV has columns "name" (image file name) and "bucket_name".
    def udf_anonymize(name, bucket_name):
        return anonymize_image_and_save(name, bucket_name, model_path, license_path)

    anonymize_udf = udf(udf_anonymize, StringType())

    # Add a new column with anonymization result (as a JSON string)
    df_out = df.withColumn("anonymization_result", anonymize_udf(df["name"], df["bucket_name"]))

    # Write the resulting DataFrame to OSS
    write_data(df_out, data_format, save_mode, output_path)

    spark.stop()


if __name__ == "__main__":
    main()
