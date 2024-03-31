import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_CLIENT_ID

from .api_client import ApiClient
from .const import DOMAIN, CONF_PWD, CONF_UCI, CONF_TITLE

_LOGGER = logging.getLogger(__name__)


async def try_auth(data):
    client_id = data.get(CONF_CLIENT_ID)
    uci = data.get(CONF_UCI)
    pwd = data.get(CONF_PWD)

    tracker = ApiClient(client_id=client_id, uci=uci, pwd=pwd)
    success = await tracker.update()
    return success


class CitizenshipTrackerConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            success = await try_auth(user_input)
            if success:
                await self.async_set_unique_id(
                    f"citizenship-application-tracker-{user_input[CONF_UCI].lower()}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=CONF_TITLE, data=user_input)
            else:
                errors["base"] = "auth_error"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_UCI): str,
                vol.Required(CONF_PWD): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
