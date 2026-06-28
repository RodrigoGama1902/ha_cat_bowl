"""Sensor entities for Cat Bowl."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
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
    async_add_entities(
        [
            CatFoodCoverageSensor(coordinator, entry),
            CatFoodLatencySensor(coordinator, entry),
            CatBowlCameraSensor(coordinator, entry),
            CatBowlScanIntervalSensor(coordinator, entry),
        ]
    )


class CatFoodCoverageSensor(CoordinatorEntity, SensorEntity):
    _attr_native_unit_of_measurement = "%"
    _attr_suggested_display_precision = 0
    _attr_icon = "mdi:bowl"

    def __init__(self, coordinator: CatBowlCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_name = "Cat Food Coverage"
        self._attr_unique_id = f"{entry.entry_id}_coverage"

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return round(self.coordinator.data.get("coverage", 0.0) * 100, 1)


class CatFoodLatencySensor(CoordinatorEntity, SensorEntity):
    _attr_native_unit_of_measurement = "ms"
    _attr_icon = "mdi:timer-outline"

    def __init__(self, coordinator: CatBowlCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_name = "Cat Food Detector Latency"
        self._attr_unique_id = f"{entry.entry_id}_latency"

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("latency_ms")


class CatBowlCameraSensor(SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:camera"

    def __init__(self, coordinator: CatBowlCoordinator, entry: ConfigEntry) -> None:
        self._attr_name = "Cat Bowl Camera"
        self._attr_unique_id = f"{entry.entry_id}_camera"
        self._attr_native_value = coordinator.camera_entity


class CatBowlScanIntervalSensor(SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = "s"
    _attr_icon = "mdi:timer-sync-outline"

    def __init__(self, coordinator: CatBowlCoordinator, entry: ConfigEntry) -> None:
        self._attr_name = "Cat Bowl Scan Interval"
        self._attr_unique_id = f"{entry.entry_id}_scan_interval"
        self._attr_native_value = coordinator.scan_interval
