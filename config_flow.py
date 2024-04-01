import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from .api_client import ApiClient
from .const import DOMAIN, CONF_PWD, CONF_UCI

_LOGGER = logging.getLogger(__name__)


async def try_auth(data):
    uci = data.get(CONF_UCI)
    pwd = data.get(CONF_PWD)

    tracker = ApiClient(uci=uci, pwd=pwd)
    success = await tracker.update()
    return success


class CitizenshipTrackerConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            success = await try_auth(user_input)
            if success:
                title = f"uci-{user_input[CONF_UCI][-4:]}"
                await self.async_set_unique_id(title)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=title, data=user_input)
            else:
                errors["base"] = "auth_error"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_UCI): str,
                vol.Required(CONF_PWD): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
