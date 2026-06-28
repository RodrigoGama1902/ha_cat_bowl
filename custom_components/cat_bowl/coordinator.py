"""Data update coordinator for Cat Bowl."""

import logging
from datetime import timedelta

import aiohttp
from homeassistant.components.camera import async_get_image
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class CatBowlCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass,
        host: str,
        port: int,
        camera_entity: str,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        self.host = host
        self.port = port
        self.camera_entity = camera_entity
        self.scan_interval = scan_interval
        self._session = async_get_clientsession(hass)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=(
                timedelta(seconds=scan_interval) if scan_interval > 0 else None
            ),
        )

    async def _async_update_data(self) -> dict:
        url = f"http://{self.host}:{self.port}/detect"
        try:
            image = await async_get_image(self.hass, self.camera_entity)
        except HomeAssistantError as err:
            raise UpdateFailed(
                f"Could not get a snapshot from {self.camera_entity}: {err}"
            ) from err

        form = aiohttp.FormData()
        form.add_field(
            "image",
            image.content,
            filename="snapshot.jpg",
            content_type=image.content_type,
        )
        try:
            async with self._session.post(
                url, data=form, timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status != 200:
                    raise UpdateFailed(
                        f"Unexpected HTTP status from Cat Bowl detect: {resp.status}"
                    )
                return await resp.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(
                f"Error communicating with Cat Bowl at {url}: {err}"
            ) from err
