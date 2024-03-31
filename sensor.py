import datetime

from dateutil import tz
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_client import ApiClient
from .coordinator import CitizenshipTrackerCoordinator


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
