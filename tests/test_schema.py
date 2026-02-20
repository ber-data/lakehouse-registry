"""Basic tests for the ber_data_registry schema."""

from ber_data_registry.datamodel import MAIN_SCHEMA_PATH


def test_schema_exists():
    """Verify the main schema file is present."""
    assert MAIN_SCHEMA_PATH.exists(), f"Schema not found at {MAIN_SCHEMA_PATH}"
