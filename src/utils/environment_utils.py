import os

def get_env_var(key: str) -> str:
    """
    Retrieves an environment variable value.
    
    Args:
        key (str): Name of the environment variable.
    
    Returns:
        str: Value of the environment variable.
    
    Raises:
        Exception: If the environment variable is not found.
    """
    value = os.getenv(key)
    if value is None:
        raise Exception(f"Environment variable `{key}` not found")
    return value
