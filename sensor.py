import datetime
import logging

from dateutil import tz
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_client import ApiClient
from .const import DOMAIN
from .coordinator import CitizenshipTrackerCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coord: CitizenshipTrackerCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [CitizenshipTrackerSensor(coord)]
    )


class CitizenshipTrackerSensor(CoordinatorEntity, SensorEntity):
    _tracker: ApiClient

    def __init__(self, coordinator: CitizenshipTrackerCoordinator):
        super().__init__(coordinator)
        self._tracker = coordinator.tracker
        self.entity_description = SensorEntityDescription(
            key="timestamp",
            translation_key="timestamp",
            device_class=SensorDeviceClass.TIMESTAMP,
        )

    @property
    def native_value(self):
        epoch = self._tracker.last_updated_epoch_ms / 1000
        return datetime.datetime.fromtimestamp(epoch, tz.UTC)
