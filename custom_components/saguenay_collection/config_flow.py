import requests
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CITIES, BASE_URL

class SaguenayCollectionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    def __init__(self):
        self.city_id = None
        self.civic_number = None
        self.streets = None

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.city_id = user_input["city"]
            self.civic_number = user_input["civic_number"]

            # Fetch streets based on city and civic number
            try:
                streets = await self.hass.async_add_executor_job(
                    self._fetch_streets, self.city_id, self.civic_number
                )
                if not streets:
                    return self.async_show_form(
                        step_id="user",
                        data_schema=self._get_user_schema(),
                        errors={"base": "no_streets_found"},
                    )
                self.streets = streets
                return await self.async_step_street()
            except Exception:
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_user_schema(),
                    errors={"base": "cannot_connect"},
                )

        return self.async_show_form(step_id="user", data_schema=self._get_user_schema())

    async def async_step_street(self, user_input=None):
        if user_input is not None:
            street_id = user_input["street"]

            # Fetch collection schedule IDs
            try:
                schedules = await self.hass.async_add_executor_job(
                    self._fetch_schedule_ids, street_id
                )
                return self.async_create_entry(
                    title="Saguenay Collection Schedule",
                    data={
                        "city": self.city_id,
                        "civic_number": self.civic_number,
                        "street_id": street_id,
                        "schedules": schedules,
                    },
                )
            except Exception:
                return self.async_show_form(
                    step_id="street",
                    data_schema=self._get_street_schema(),
                    errors={"base": "cannot_connect"},
                )

        return self.async_show_form(step_id="street", data_schema=self._get_street_schema())

    @staticmethod
    def _fetch_streets(city_id, civic_number):
        response = requests.post(
            f"{BASE_URL}/getrues",
            data={"no_civique": civic_number, "no_ville": city_id},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _fetch_schedule_ids(street_id):
        response = requests.post(
            f"{BASE_URL}/getcollecteinfo",
            data={"ide": street_id},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def _get_user_schema(self):
        return vol.Schema(
            {
                vol.Required("city"): vol.In(CITIES),
                vol.Required("civic_number"): str,
            }
        )

    def _get_street_schema(self):
        return vol.Schema(
            {
                vol.Required("street"): vol.In(
                    {street["id"]: street["value"] for street in self.streets}
                )
            }
        )
