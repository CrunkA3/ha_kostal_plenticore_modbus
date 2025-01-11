import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE

from homeassistant.components.number import (
    NumberEntity
)

from homeassistant.core import (
    HomeAssistant,
    callback
)

from .coordinator import (
    InverterCoordinator
)

from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    MANUFACTURER,
    MODEL,
    NAME
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the EEVE Mower battery sensor from a config entry."""
    _LOGGER.info("async_setup_entry")
    ip_address = entry.data[CONF_IP_ADDRESS]

    #Add mowing info sensors
    inverter_coordinator = entry.runtime_data.inverter_coordinator
    async_add_entities([
        MinimumSocNumber(inverter_coordinator, ip_address),
        MaximumSocNumber(inverter_coordinator, ip_address)
        ])


class  KostalModbusNumber(CoordinatorEntity, NumberEntity):
    """number input."""
    
    _attr_mode = "slider"
    _attr_native_min_value = 5
    _attr_native_step = 5
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address, property_name, modbus_address, name, icon, unit):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._state = None
        self._name = name
        self._unique_id = f"{property_name}_number_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"
        self._property_name = property_name
        self._modbus_address = modbus_address
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_info(self):
        """Get information about this device."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": NAME,
            "manufacturer": MANUFACTURER,
            "model": MODEL,
        }

    @property
    def native_value(self):
        return self.coordinator.data[self._property_name]
        #return 0


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        _LOGGER.info("async update")
        await self.coordinator.async_request_refresh()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.coordinator.async_set_float_alue(self._modbus_address, value)





class  MinimumSocNumber(KostalModbusNumber):
    """Minimum Battery SoC Number Input."""

    def __init__(self, coordinator, ip_address):
        super().__init__(coordinator, ip_address, "min_soc", 1042, "Mininum SoC", "mdi:battery-10", "%")

class  MaximumSocNumber(KostalModbusNumber):
    """Maximum Battery SoC Number Input."""

    def __init__(self, coordinator, ip_address):
        super().__init__(coordinator, ip_address, "max_soc", 1044, "Maximum SoC", "mdi:battery-90", "%")