import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_CLIENT_ID
from homeassistant.core import HomeAssistant

from .api_client import ApiClient
from .const import CONF_UCI, CONF_PWD, COORDINATOR_NAME, DOMAIN
from .coordinator import CitizenshipTrackerCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    client_id = config_entry.data.get(CONF_CLIENT_ID)
    uci = config_entry.data.get(CONF_UCI)
    pwd = config_entry.data.get(CONF_PWD)

    tracker = ApiClient(client_id=client_id, uci=uci, pwd=pwd)
    coord = CitizenshipTrackerCoordinator(
        hass, tracker, COORDINATOR_NAME
    )

    await coord.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coord

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    hass.data[DOMAIN].pop(config_entry.entry_id)
    return unload_ok
