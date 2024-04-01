import datetime
import logging

from dateutil import tz
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


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coord: CitizenshipTrackerCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([CitizenshipTrackerSensor(coord)])


class CitizenshipTrackerSensor(CoordinatorEntity, SensorEntity):
    _tracker: ApiClient

    def __init__(self, coordinator: CitizenshipTrackerCoordinator):
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key="timestamp",
            translation_key="timestamp",
            device_class=SensorDeviceClass.TIMESTAMP,
        )
        self._tracker = coordinator.tracker
        self._attr_unique_id = f"{coordinator.config_entry.title}-{self.entity_description.key}"
        self._attr_has_entity_name = True
        self._attr_device_info = device_info(coordinator.config_entry)

    @property
    def native_value(self):
        epoch = self._tracker.last_updated_epoch_ms / 1000
        return datetime.datetime.fromtimestamp(epoch, tz.UTC)


def device_info(config_entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, config_entry.entry_id)},
        name=config_entry.title,
    )
