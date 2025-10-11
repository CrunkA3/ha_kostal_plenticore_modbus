import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass
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
        BatteryWorkCapacitySensor(inverter_coordinator, ip_address),
        PowerScaleFactorSensor(inverter_coordinator, ip_address),
        MaxChargePowerSensor(inverter_coordinator, ip_address),
        MaxDischargePowerSensor(inverter_coordinator, ip_address),
        CurrentDcSensor(inverter_coordinator, ip_address, 1, 258),
        CurrentDcSensor(inverter_coordinator, ip_address, 2, 268),
        CurrentDcSensor(inverter_coordinator, ip_address, 3, 278),
        PowerDcSensor(inverter_coordinator, ip_address, 1, 260),
        PowerDcSensor(inverter_coordinator, ip_address, 2, 270),
        PowerDcSensor(inverter_coordinator, ip_address, 3, 280),
        VoltageDcSensor(inverter_coordinator, ip_address, 1, 266),
        VoltageDcSensor(inverter_coordinator, ip_address, 2, 276),
        VoltageDcSensor(inverter_coordinator, ip_address, 3, 286)
        ])


class BatteryWorkCapacitySensor(CoordinatorEntity, SensorEntity):
    """Battery work capacity sensor."""
    
    _attr_icon = "mdi:battery"
    _attr_device_class = "energy_storage"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "Wh"
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._state = None
        self._name = "Battery work capacity"
        self._unique_id = f"battery_work_capacity_sensor_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data["batteryWorkCapacity"]
        #return 0


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        _LOGGER.info("async update")
        await self.coordinator.async_request_refresh()



class PowerScaleFactorSensor(CoordinatorEntity, SensorEntity):
    """ Power Scale Factor sensor."""
    
    _attr_icon = "mdi:function-variant"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._state = None
        self._name = "Power Scale Factor"
        self._unique_id = f"power_scale_factor_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data["scaleFactor"]
        #return 0


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        _LOGGER.info("async update")
        await self.coordinator.async_request_refresh()



class MaxChargePowerSensor(CoordinatorEntity, SensorEntity):
    """Battery Maximum charge power limit sensor."""
    
    _attr_icon = "mdi:battery-charging-90"
    _attr_device_class = "power"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._state = None
        self._name = "Maximum Charge Power"
        self._unique_id = f"max_charge_power_sensor_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data["maxChargePower"]
        #return 0


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()






class MaxDischargePowerSensor(CoordinatorEntity, SensorEntity):
    """Battery Maximum discharge power limit sensor."""
    
    _attr_icon = "mdi:battery-charging-10"
    _attr_device_class = "power"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._state = None
        self._name = "Maximum Discharge Power"
        self._unique_id = f"max_discharge_power_sensor_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data["maxDischargePower"]
        #return 0


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()




class CurrentDcSensor(CoordinatorEntity, SensorEntity):
    """Current DC sensor."""
    
    _attr_icon = "mdi:current-dc"
    _attr_device_class = "current"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "A"
    _attr_suggested_display_precision = 2

    def __init__(self, coordinator, ip_address, dc_number, register_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._dc_number = dc_number
        self._register_address = register_address
        self._state = None

        self._name = f"Current DC {dc_number}"
        self._unique_id = f"current_dc_sensor_{dc_number}_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data[f"current_dc_{self._dc_number}"]


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()


class PowerDcSensor(CoordinatorEntity, SensorEntity):
    """Power DC sensor."""
    
    _attr_icon = "mdi:flash"
    _attr_device_class = "power"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address, dc_number, register_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._dc_number = dc_number
        self._register_address = register_address
        self._state = None

        self._name = f"Power DC {dc_number}"
        self._unique_id = f"power_dc_sensor_{dc_number}_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data[f"power_dc_{self._dc_number}"]


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()


class VoltageDcSensor(CoordinatorEntity, SensorEntity):
    """Voltage DC sensor."""
    
    _attr_icon = "mdi:sine-wave"
    _attr_device_class = "voltage"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "V"
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, ip_address, dc_number, register_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._dc_number = dc_number
        self._register_address = register_address
        self._state = None

        self._name = f"Voltage DC {dc_number}"
        self._unique_id = f"voltage_dc_sensor_{dc_number}_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

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
    def state(self):
        return self.coordinator.data[f"voltage_dc_{self._dc_number}"]


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()