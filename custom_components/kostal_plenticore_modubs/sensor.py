"""
Sensor platform for Kostal Plenticore inverters.
This module defines various sensor entities
that represent different parameters and states of the Kostal Plenticore inverter.
The sensors are updated using a coordinator
that fetches data from the inverter at regular intervals.
"""

import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN, CONF_IP_ADDRESS, MANUFACTURER, MODEL, NAME

from .register_info import REGISTERS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    _LOGGER.info("async_setup_entry")
    ip_address = entry.data[CONF_IP_ADDRESS]

    # add sensors
    inverter_coordinator = entry.runtime_data.inverter_coordinator
    sensors = [
        InverterStateSensor(inverter_coordinator, ip_address, 56),
        ControllerTemperatureSensor(inverter_coordinator, ip_address, 98),
        MaxChargePowerSensor(inverter_coordinator, ip_address, 1076),
        MaxDischargePowerSensor(inverter_coordinator, ip_address, 1078),
    ]

    # add sensors from registers
    for ri in REGISTERS:
        match ri.type:
            case "U16":
                sensors.append(
                    KostalUInt16Sensor(
                        inverter_coordinator,
                        ip_address,
                        ri.address,
                        ri.unique_id,
                        ri.name,
                        ri.icon,
                        ri.device_class,
                        ri.unit,
                        ri.display_precision,
                        ri.sensor_state_class,
                    )
                )
            case "S16":
                sensors.append(
                    KostalInt16Sensor(
                        inverter_coordinator,
                        ip_address,
                        ri.address,
                        ri.unique_id,
                        ri.name,
                        ri.icon,
                        ri.device_class,
                        ri.unit,
                        ri.display_precision,
                        ri.sensor_state_class,
                    )
                )
            case "U32":
                sensors.append(
                    KostalUInt32Sensor(
                        inverter_coordinator,
                        ip_address,
                        ri.address,
                        ri.unique_id,
                        ri.name,
                        ri.icon,
                        ri.device_class,
                        ri.unit,
                        ri.display_precision,
                        ri.sensor_state_class,
                    )
                )
            case "S32":
                sensors.append(
                    KostalInt32Sensor(
                        inverter_coordinator,
                        ip_address,
                        ri.address,
                        ri.unique_id,
                        ri.name,
                        ri.icon,
                        ri.device_class,
                        ri.unit,
                        ri.display_precision,
                        ri.sensor_state_class,
                    )
                )
            case "Float":
                sensors.append(
                    KostalFloat32Sensor(
                        inverter_coordinator,
                        ip_address,
                        ri.address,
                        ri.unique_id,
                        ri.name,
                        ri.icon,
                        ri.device_class,
                        ri.unit,
                        ri.display_precision,
                        ri.sensor_state_class,
                    )
                )

    async_add_entities(sensors)


class KostalSensor(CoordinatorEntity, SensorEntity):
    """Kostal sensor."""

    _attr_icon = None
    _attr_device_class = None
    _attr_native_unit_of_measurement = None
    _attr_suggested_display_precision = None

    def __init__(
        self,
        coordinator,
        ip_address,
        register_address,
        unique_id,
        name,
        icon,
        device_class,
        native_unit_of_measurement,
        suggested_display_precision,
        sensor_state_class=SensorStateClass.MEASUREMENT,
    ):
        super().__init__(coordinator, context=0)

        self._register_address = register_address

        self._name = name
        self._unique_id = f"{unique_id}_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = native_unit_of_measurement
        self._attr_suggested_display_precision = suggested_display_precision
        self._attr_state_class = sensor_state_class

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()


class KostalFloat32Sensor(KostalSensor):
    """Kostal FLOAT32 sensor."""

    def __init__(
        self,
        coordinator,
        ip_address,
        register_address,
        unique_id,
        name,
        icon,
        device_class,
        native_unit_of_measurement,
        suggested_display_precision,
        sensor_state_class=SensorStateClass.MEASUREMENT,
    ):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            unique_id,
            name,
            icon,
            device_class,
            native_unit_of_measurement,
            suggested_display_precision,
            sensor_state_class,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.read_float32(self._register_address)


class KostalInt16Sensor(KostalSensor):
    """Kostal INT16 sensor."""

    def __init__(
        self,
        coordinator,
        ip_address,
        register_address,
        unique_id,
        name,
        icon,
        device_class,
        native_unit_of_measurement,
        suggested_display_precision,
        sensor_state_class=SensorStateClass.MEASUREMENT,
    ):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            unique_id,
            name,
            icon,
            device_class,
            native_unit_of_measurement,
            suggested_display_precision,
            sensor_state_class,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.read_int16(self._register_address)


class KostalUInt16Sensor(KostalSensor):
    """Kostal UINT16 sensor."""

    def __init__(
        self,
        coordinator,
        ip_address,
        register_address,
        unique_id,
        name,
        icon,
        device_class,
        native_unit_of_measurement,
        suggested_display_precision,
        sensor_state_class=SensorStateClass.MEASUREMENT,
    ):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            unique_id,
            name,
            icon,
            device_class,
            native_unit_of_measurement,
            suggested_display_precision,
            sensor_state_class,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.read_uint16(self._register_address)


class KostalInt32Sensor(KostalSensor):
    """Kostal INT32 sensor."""

    def __init__(
        self,
        coordinator,
        ip_address,
        register_address,
        unique_id,
        name,
        icon,
        device_class,
        native_unit_of_measurement,
        suggested_display_precision,
        sensor_state_class=SensorStateClass.MEASUREMENT,
    ):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            unique_id,
            name,
            icon,
            device_class,
            native_unit_of_measurement,
            suggested_display_precision,
            sensor_state_class,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.read_int32(self._register_address)


class KostalUInt32Sensor(KostalSensor):
    """Kostal UINT32 sensor."""

    def __init__(
        self,
        coordinator,
        ip_address,
        register_address,
        unique_id,
        name,
        icon,
        device_class,
        native_unit_of_measurement,
        suggested_display_precision,
        sensor_state_class=SensorStateClass.MEASUREMENT,
    ):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            unique_id,
            name,
            icon,
            device_class,
            native_unit_of_measurement,
            suggested_display_precision,
            sensor_state_class,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.read_uint32(self._register_address)


class MaxChargePowerSensor(KostalFloat32Sensor):
    """Battery Maximum charge power limit sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            "max_charge_power_sensor",
            "Maximum Charge Power",
            "mdi:battery-charging-90",
            "power",
            "W",
            0,
        )


class MaxDischargePowerSensor(KostalFloat32Sensor):
    """Battery Maximum discharge power limit sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            "max_discharge_power_sensor",
            "Maximum Discharge Power",
            "mdi:battery-charging-10",
            "power",
            "W",
            0,
        )


class ControllerTemperatureSensor(KostalFloat32Sensor):
    """Temperature of controller PCB sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(
            coordinator,
            ip_address,
            register_address,
            "controller_temperature_sensor",
            "Controller Temperature",
            "mdi:thermometer",
            "TEMPERATURE",
            "°C",
            1,
        )


class InverterStateSensor(CoordinatorEntity, SensorEntity):
    """Inverter State sensor."""

    _attr_icon = "mdi:state-machine"
    _attr_device_class = "enum"

    _options_enum = [
        "Off",
        "Init",
        "IsoMeas",
        "GridCheck",
        "StartUp",
        "-",
        "FeedIn",
        "Throttled",
        "ExtSwitchOff",
        "Update",
        "Standby",
        "GridSync",
        "GridPreCheck",
        "GridSwitchOff",
        "Overheating",
        "Shutdown",
        "ImproperDcVoltage",
        "ESB",
        "Unknown",
    ]

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._register_address = register_address
        self._state = None

        self._name = "Inverter State"
        self._unique_id = f"inverter_state_sensor_{ip_address.replace('.', '_')}"
        self._device_id = f"{NAME}_{ip_address.replace('.', '_')}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
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
        """Return the state of the sensor."""
        inverter_state = self.coordinator.data["inverter_state"]
        return self._options_enum[inverter_state]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()

    @property
    def options(self):
        """Return the list of available options."""
        return list(self._options_enum)
