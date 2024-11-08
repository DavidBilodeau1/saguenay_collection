import logging
import requests
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .const import DOMAIN, BASE_URL

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

async def async_setup_entry(hass, config_entry, async_add_entities):
    city_id = config_entry.data["city"]
    civic_number = config_entry.data["civic_number"]
    street_id = config_entry.data["street_id"]
    schedules = config_entry.data["schedules"]

    coordinator = CollectionCoordinator(hass, city_id, civic_number, street_id, schedules)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        CollectionSensor(coordinator, "compostage"),
        CollectionSensor(coordinator, "ordure"),
        CollectionSensor(coordinator, "recyclage"),
    ]
    async_add_entities(sensors)

class CollectionCoordinator(DataUpdateCoordinator):
    """Fetch collection data."""

    def __init__(self, hass, city_id, civic_number, street_id, schedules):
        """Initialize the coordinator."""
        self.city_id = city_id
        self.civic_number = civic_number
        self.street_id = street_id
        self.schedules = schedules  # Store schedules as a list initially
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        _LOGGER.debug("Fetching collection schedule for street ID %s", self.street_id)

        def fetch_data():
            results = {}
            for schedule in self.schedules:
                try:
                    schedule_type = schedule.get("nom", "Unknown").lower()
                    horaire_id = schedule.get("horaire_id")

                    _LOGGER.debug("Fetching data for schedule: %s with horaire_id: %s", schedule_type, horaire_id)
                    response = requests.post(
                        f"{BASE_URL}/getcedule",
                        data={"horaire_id": horaire_id},
                        timeout=15,
                    )
                    response.raise_for_status()
                    data = response.json()
                    results[schedule_type] = data["date_collecte"]
                except requests.exceptions.RequestException as e:
                    _LOGGER.error("Error fetching data for %s: %s", schedule_type, e)
                except ValueError as e:
                    _LOGGER.error("Error parsing JSON for %s: %s", schedule_type, e)
            _LOGGER.debug(results)
            return results

        return await self.hass.async_add_executor_job(fetch_data)

class CollectionSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, collection_type):
        super().__init__(coordinator)
        self._collection_type = collection_type

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Saguenay {self._collection_type.capitalize()} Schedule"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._collection_type, "No data available")

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"saguenay_collection_{self._collection_type}_{self.coordinator.street_id}"

    @property
    def device_class(self):
        """Return the device class."""
        return "timestamp"
