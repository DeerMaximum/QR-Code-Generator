"""QR Generator image platform."""

from __future__ import annotations

import io
from typing import Any

from PIL import ImageColor
import pyqrcode

from homeassistant.util import dt as dt_util
from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_VALUE_TEMPLATE
from homeassistant.core import HomeAssistant, callback, Event, EventStateChangedData
from homeassistant.helpers import template
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    _LOGGER,
    ATTR_BACKGROUND_COLOR,
    ATTR_BORDER,
    ATTR_COLOR,
    ATTR_ERROR_CORRECTION,
    ATTR_SCALE,
    ATTR_TEXT,
    CONF_BACKGROUND_COLOR,
    CONF_BORDER,
    CONF_COLOR,
    CONF_ERROR_CORRECTION,
    CONF_SCALE,
    DEFAULT_BACKGROUND_COLOR,
    DEFAULT_BORDER,
    DEFAULT_COLOR,
    DEFAULT_ERROR_CORRECTION,
    DEFAULT_SCALE,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entries."""

    entity = QRImage(config_entry, hass)

    async_add_entities([entity])


class QRImage(ImageEntity):
    """Representation of a QR code."""

    def __init__(self, entry: ConfigEntry, hass: HomeAssistant) -> None:
        """Initialize the camera."""
        super().__init__(hass)

        self.hass: HomeAssistant = hass

        self.image: io.BytesIO = io.BytesIO()

        self.value_template: str = entry.data[CONF_VALUE_TEMPLATE]
        self.template = template.Template(self.value_template, self.hass)  # type: ignore[no-untyped-call]
        self.rendered_template: template.RenderInfo = template.RenderInfo(self.template)

        self.color_hex = entry.data.get(CONF_COLOR, DEFAULT_COLOR)
        self.color = ImageColor.getcolor(self.color_hex, "RGBA")

        self.background_color_hex = entry.data.get(
            CONF_BACKGROUND_COLOR, DEFAULT_BACKGROUND_COLOR
        )
        self.background_color = ImageColor.getcolor(self.background_color_hex, "RGBA")

        self.scale: int = entry.data.get(CONF_SCALE, DEFAULT_SCALE)
        self.border: int = entry.data.get(CONF_BORDER, DEFAULT_BORDER)
        self.error_correction: str = entry.data.get(
            CONF_ERROR_CORRECTION, DEFAULT_ERROR_CORRECTION
        )

        self._attr_name: str = entry.data[CONF_NAME]
        self._attr_unique_id: str = f"{entry.entry_id}-qr-code"
        self._attr_content_type: str = "image/png"

    def _render(self) -> None:
        """Render template."""
        self.rendered_template = self.template.async_render_to_info()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""

        self._render()
        await self._refresh()

        @callback
        async def _update(event: Event[EventStateChangedData]) -> None:
            """Handle state changes."""
            old_state = event.data["old_state"]
            new_state = event.data["new_state"]

            if old_state is None or new_state is None:
                return

            if old_state.state == new_state.state:
                return

            self._render()
            await self._refresh()

        async_track_state_change_event(
            self.hass, list(self.rendered_template.entities), _update
        )

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        return self.image.getvalue()

    async def _refresh(self) -> None:
        """Create the QR code."""

        _LOGGER.debug('Print "%s" with: %s', self.name, self.rendered_template.result())

        code = pyqrcode.create(
            self.rendered_template.result(), error=self.error_correction
        )

        self.image = io.BytesIO()
        code.png(
            self.image,
            scale=self.scale,
            module_color=self.color,
            background=self.background_color,
            quiet_zone=self.border,
        )

        self._attr_image_last_updated = dt_util.utcnow()
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes of the sensor."""
        return {
            ATTR_TEXT: self.rendered_template.result(),
            ATTR_COLOR: self.color_hex,
            ATTR_BACKGROUND_COLOR: self.background_color_hex,
            ATTR_SCALE: self.scale,
            ATTR_BORDER: self.border,
            ATTR_ERROR_CORRECTION: self.error_correction,
        }
