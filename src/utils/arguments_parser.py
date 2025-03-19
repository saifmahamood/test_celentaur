import argparse

def parse_arguments():
    """
    Parses command-line arguments for the Spark job.
    
    Returns:
        Namespace: Parsed arguments containing input, output, format, and save mode.
    """
    parser = argparse.ArgumentParser(description="Spark job argument parser")
    parser.add_argument("--input", required=True, help="OSS input path")
    parser.add_argument("--output", required=True, help="OSS output path")
    parser.add_argument("--format", default="parquet", help="Data format (default: parquet)")
    parser.add_argument("--save-mode", default="overwrite", help="Save mode (default: overwrite)")
    return parser.parse_args()
