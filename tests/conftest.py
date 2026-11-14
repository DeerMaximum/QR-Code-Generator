"""Fixtures for testing."""
import pytest


@pytest.fixture
async def mock_recorder_before_hass(async_setup_recorder_instance) -> None:
    """Set up the recorder before hass, for tests that use recorder_mock."""
