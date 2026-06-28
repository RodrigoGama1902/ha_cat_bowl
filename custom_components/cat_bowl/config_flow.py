"""Config flow for Cat Bowl."""

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required("host", default=DEFAULT_HOST): str,
        vol.Required("port", default=DEFAULT_PORT): int,
        vol.Required("camera_entity"): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="camera")
        ),
        vol.Optional(
            "scan_interval", default=DEFAULT_SCAN_INTERVAL
        ): vol.All(vol.Coerce(int), vol.Range(min=0)),
    }
)


async def _validate_connection(hass: HomeAssistant, host: str, port: int) -> None:
    """Raise if the server is unreachable."""
    url = f"http://{host}:{port}/health"
    session = async_get_clientsession(hass)
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
        resp.raise_for_status()


class CatBowlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CatBowlOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input['host']}:{user_input['port']}"
            )
            self._abort_if_unique_id_configured()
            try:
                await _validate_connection(
                    self.hass, user_input["host"], user_input["port"]
                )
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Cat Bowl ({user_input['host']}:{user_input['port']})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )


class CatBowlOptionsFlow(config_entries.OptionsFlow):
    """Allow editing all settings after the integration is set up."""

    def __init__(self, config_entry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        current = {**self._entry.data, **self._entry.options}

        if user_input is not None:
            try:
                await _validate_connection(
                    self.hass, user_input["host"], user_input["port"]
                )
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Required("host", default=current["host"]): str,
                vol.Required("port", default=current["port"]): int,
                vol.Required(
                    "camera_entity", default=current["camera_entity"]
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="camera")
                ),
                vol.Optional(
                    "scan_interval", default=current["scan_interval"]
                ): vol.All(vol.Coerce(int), vol.Range(min=0)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
        )
