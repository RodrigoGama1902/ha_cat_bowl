"""Button entities for Cat Bowl."""

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import CatBowlCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CatBowlCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CatBowlRefreshButton(coordinator, entry)])


class CatBowlRefreshButton(ButtonEntity):
    _attr_icon = "mdi:refresh"

    def __init__(self, coordinator: CatBowlCoordinator, entry: ConfigEntry) -> None:
        self._coordinator = coordinator
        self._attr_name = "Cat Bowl Refresh"
        self._attr_unique_id = f"{entry.entry_id}_refresh"

    async def async_press(self) -> None:
        """Capture a new snapshot and update the detection values."""
        await self._coordinator.async_request_refresh()
