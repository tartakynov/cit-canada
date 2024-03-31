import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_CLIENT_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from api_client import ApiClient
from const import CONF_UCI, CONF_PWD, COORDINATOR_NAME
from coordinator import CitizenshipTrackerCoordinator
from sensor import CitizenshipTrackerSensor

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client_id = config_entry.data.get(CONF_CLIENT_ID)
    uci = config_entry.data.get(CONF_UCI)
    pwd = config_entry.data.get(CONF_PWD)

    tracker = ApiClient(client_id=client_id, uci=uci, pwd=pwd)
    coord = CitizenshipTrackerCoordinator(
        hass, tracker, COORDINATOR_NAME
    )

    await coord.async_config_entry_first_refresh()
    async_add_entities(
        [CitizenshipTrackerSensor(coord)]
    )
