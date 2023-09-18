import os

from homeassistant.components.image import ImageEntity
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import async_get_platforms

from custom_components.qr_generator import DOMAIN
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from custom_components.qr_generator.const import ATTR_FILENAME, _LOGGER


def register_services(hass: HomeAssistant) -> None:
    """Register the services."""

    async def save_image(service_call: ServiceCall) -> None:
        """Save the image to path."""
        entity_id = service_call.data[ATTR_ENTITY_ID]
        filepath = service_call.data[ATTR_FILENAME]

        if not hass.config.is_allowed_path(filepath):
            raise HomeAssistantError(
                f"Cannot write `{filepath}`, no access to path; `allowlist_external_dirs` may need to be adjusted in `configuration.yaml`"
            )

        platform = async_get_platforms(hass, DOMAIN)

        if len(platform) < 1:
            raise HomeAssistantError(
                f"Integration not found: {DOMAIN}"
            )

        entity: ImageEntity | None = platform[0].entities.get(entity_id, None)

        if not entity:
            raise HomeAssistantError(
                f"Could not find entity {entity_id} from integration {DOMAIN}"
            )

        image = await entity.async_image()

        def _write_image(to_file: str, image_data: bytes) -> None:
            """Executor helper to write image."""
            os.makedirs(os.path.dirname(to_file), exist_ok=True)
            with open(to_file, "wb") as img_file:
                img_file.write(image_data)

        try:
            await hass.async_add_executor_job(_write_image, filepath, image)
        except OSError as err:
            _LOGGER.error("Can't write image to file: %s", err)

    hass.services.async_register(DOMAIN, "save", save_image, vol.Schema({
        vol.Required(ATTR_ENTITY_ID) : cv.entity_id,
        vol.Required(ATTR_FILENAME): cv.string
    }))


