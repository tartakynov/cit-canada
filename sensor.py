import datetime
import logging
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass, SensorEntityDescription, SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_client import ApiClient
from .const import DOMAIN
from .coordinator import CitizenshipTrackerCoordinator

_LOGGER = logging.getLogger(__name__)


def sensor_fn_application_updated_at(tracker: ApiClient) -> datetime.datetime:
    return tracker.application_updated_at


def sensor_fn_data_synced_at(tracker: ApiClient) -> datetime.datetime:
    return tracker.data_synced_at


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coord: CitizenshipTrackerCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        CitizenshipTrackerSensor(
            coordinator=coord,
            value_fn=sensor_fn_application_updated_at,
            description=SensorEntityDescription(
                key="app_updated_at",
                translation_key="app_updated_at",
                device_class=SensorDeviceClass.TIMESTAMP,
            ),
        ),
        CitizenshipTrackerSensor(
            coordinator=coord,
            value_fn=sensor_fn_data_synced_at,
            description=SensorEntityDescription(
                key="data_synced_at",
                translation_key="data_synced_at",
                device_class=SensorDeviceClass.TIMESTAMP,
            ),
        ),
    ])


class CitizenshipTrackerSensor(CoordinatorEntity, SensorEntity):
    _tracker: ApiClient

    def __init__(self,
                 coordinator: CitizenshipTrackerCoordinator,
                 value_fn: Callable[[ApiClient], Any],
                 description: SensorEntityDescription):
        super().__init__(coordinator)
        self.entity_description = description
        self._tracker = coordinator.tracker
        self._attr_unique_id = f"{coordinator.config_entry.title}-{self.entity_description.key}"
        self._attr_has_entity_name = True
        self._attr_device_info = device_info(coordinator.config_entry)
        self._value_fn = value_fn

    @property
    def native_value(self):
        return self._value_fn(self._tracker)


def device_info(config_entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, config_entry.entry_id)},
        name=config_entry.title,
    )
