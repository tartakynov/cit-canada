import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api_client import ApiClient

_LOGGER = logging.getLogger(__name__)

DEFAULT_UPDATE_INTERVAL = timedelta(hours=6)


class CitizenshipTrackerCoordinator(DataUpdateCoordinator):
    tracker: ApiClient

    def __init__(self, hass: HomeAssistant, tracker: ApiClient, name: str):
        super().__init__(
            hass, _LOGGER, name=name, update_interval=DEFAULT_UPDATE_INTERVAL
        )
        self.tracker = tracker

    async def _async_update_data(self):
        try:
            await self.tracker.update()
        except Exception as ex:
            raise UpdateFailed(f"Error fetching {self.name} data: {ex}") from ex
        return self.tracker
