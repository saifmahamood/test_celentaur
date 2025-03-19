import pytest
import os
from utils.environment_utils import get_env_var

def test_get_env_var(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "TEST_VALUE")
    assert get_env_var("TEST_KEY") == "TEST_VALUE"
    with pytest.raises(Exception):
        get_env_var("NON_EXISTENT_KEY")
