"""Binary sensor entities for Cat Bowl."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CatBowlCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CatBowlCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CatFoodBinarySensor(coordinator, entry)])


class CatFoodBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY
    _attr_icon = "mdi:bowl-mix"

    def __init__(self, coordinator: CatBowlCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_name = "Cat Food"
        self._attr_unique_id = f"{entry.entry_id}_food"

    @property
    def is_on(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("food_present")
