import os
from celantur_bindings import CelanturProcessor

def test_full_flow():
    # Define file paths (update these paths as needed)
    license_path = "/app/celantur_sdk/license"
    model_path = "/app/celantur_sdk/yolov8_all_1280_medium_v4_static.onnx.enc"
    input_image_path = "/app/celantur_sdk/image.jpg"  # Provide a test input image
    output_image_path = "test_output.jpg"
    metadata_output_path = "metadata.json"

    # Read the test input image as bytes
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Test input image '{input_image_path}' not found.")
    with open(input_image_path, "rb") as f:
        image_bytes = f.read()

    # Create a CelanturProcessor instance
    processor = CelanturProcessor(license_path)
    print("Processor created.")

    # Load the inference model
    processor.load_inference_model(model_path)
    print("Inference model loaded.")

    # Process image and retrieve both the processed image and metadata in one call.
    result_bytes, metadata_json = processor.process_and_get_result_and_metadata(image_bytes)
    print("Processing complete.")

    # Save the anonymized image to a file.
    with open(output_image_path, "wb") as f:
        f.write(result_bytes)
    print(f"Anonymized image saved to '{output_image_path}'.")

    # Save the metadata JSON to a file.
    with open(metadata_output_path, "w") as f:
        f.write(metadata_json)
    print(f"Metadata JSON saved to '{metadata_output_path}'.")
    print("Metadata JSON:")
    print(metadata_json)

if __name__ == "__main__":
    test_full_flow()

