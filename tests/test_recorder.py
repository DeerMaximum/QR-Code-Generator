"""Test the QR Generator image's recorder exclusions."""
from datetime import timedelta

import pytest
from homeassistant.components.recorder import Recorder
from homeassistant.components.recorder.history import get_significant_states
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.components.recorder.common import (
    async_wait_recording_done,
)

from custom_components.qr_generator.const import (
    ATTR_COLOR,
    ATTR_TEXT,
    DEFAULT_COLOR,
    DOMAIN,
)

from .test_image import DUMMY_ENTRY


@pytest.fixture(autouse=True)
async def mock_recorder_before_hass(async_setup_recorder_instance) -> None:
    """Set up the recorder before hass, which conftest's autouse fixture starts."""


@pytest.mark.asyncio
async def test_text_not_recorded(recorder_mock: Recorder, hass: HomeAssistant) -> None:
    """Test that the content, which can hold a secret, isn't recorded."""
    config_entry: MockConfigEntry = MockConfigEntry(
        domain=DOMAIN, title="QR", data=DUMMY_ENTRY
    )

    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states,
        hass,
        dt_util.utcnow() - timedelta(minutes=5),
        None,
        ["image.test_qr_code"],
    )

    assert hass.states.get("image.test_qr_code").attributes.get(ATTR_TEXT) == "Sample content"
    assert len(states["image.test_qr_code"]) == 1
    assert ATTR_TEXT not in states["image.test_qr_code"][0].attributes
    assert states["image.test_qr_code"][0].attributes.get(ATTR_COLOR) == DEFAULT_COLOR
