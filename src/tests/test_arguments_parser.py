import pytest
from utils.arguments_parser import parse_arguments

def test_parse_arguments():
    test_args = ["--input", "oss://input-path", "--output", "oss://output-path"]
    parsed_args = parse_arguments(test_args)
    assert parsed_args.input == "oss://input-path"
    assert parsed_args.output == "oss://output-path"
    assert parsed_args.format == "parquet"
    assert parsed_args.save_mode == "overwrite"
