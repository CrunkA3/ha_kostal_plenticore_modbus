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

from .register_info import (
    RegisterInfo,
    REGISTERS
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the EEVE Mower battery sensor from a config entry."""
    _LOGGER.info("async_setup_entry")
    ip_address = entry.data[CONF_IP_ADDRESS]

    #Add mowing info sensors
    inverter_coordinator = entry.runtime_data.inverter_coordinator
    sensors = [
        InverterStateSensor(inverter_coordinator, ip_address, 56),
        ControllerTemperatureSensor(inverter_coordinator, ip_address, 98),
        BatteryWorkCapacitySensor(inverter_coordinator, ip_address, 1068),
        PowerScaleFactorSensor(inverter_coordinator, ip_address, 1025),
        MaxChargePowerSensor(inverter_coordinator, ip_address, 1076),
        MaxDischargePowerSensor(inverter_coordinator, ip_address, 1078),
        CurrentDcSensor(inverter_coordinator, ip_address, 1, 258),
        CurrentDcSensor(inverter_coordinator, ip_address, 2, 268),
        CurrentDcSensor(inverter_coordinator, ip_address, 3, 278),
        PowerDcSensor(inverter_coordinator, ip_address, 1, 260),
        PowerDcSensor(inverter_coordinator, ip_address, 2, 270),
        PowerDcSensor(inverter_coordinator, ip_address, 3, 280),
        VoltageDcSensor(inverter_coordinator, ip_address, 1, 266),
        VoltageDcSensor(inverter_coordinator, ip_address, 2, 276),
        VoltageDcSensor(inverter_coordinator, ip_address, 3, 286)
        ]

    for ri in REGISTERS:
        match ri.type:
            case "U16":
                sensors.append(KostalUInt16Sensor(inverter_coordinator, ip_address, ri.address, ri.unique_id, ri.name, ri.icon, ri.device_class, ri.unit, ri.display_precision, ri.sensor_state_class))
            case "S16":
                sensors.append(KostalInt16Sensor(inverter_coordinator, ip_address, ri.address, ri.unique_id, ri.name, ri.icon, ri.device_class, ri.unit, ri.display_precision, ri.sensor_state_class))
            case "U32":
                sensors.append(KostalUInt32Sensor(inverter_coordinator, ip_address, ri.address, ri.unique_id, ri.name, ri.icon, ri.device_class, ri.unit, ri.display_precision, ri.sensor_state_class))
            case "S32":
                sensors.append(KostalInt32Sensor(inverter_coordinator, ip_address, ri.address, ri.unique_id, ri.name, ri.icon, ri.device_class, ri.unit, ri.display_precision, ri.sensor_state_class))
            case "Float":
                sensors.append(KostalFloat32Sensor(inverter_coordinator, ip_address, ri.address, ri.unique_id, ri.name, ri.icon, ri.device_class, ri.unit, ri.display_precision, ri.sensor_state_class))

    async_add_entities(sensors)

class KostalSensor(CoordinatorEntity, SensorEntity):
    """ Kostal sensor."""
    
    _attr_icon = None
    _attr_device_class = None
    _attr_native_unit_of_measurement = None
    _attr_suggested_display_precision = None

    def __init__(self, coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class = SensorStateClass.MEASUREMENT):
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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


    async def async_update(self):
        """Synchronize state"""
        await self.coordinator.async_request_refresh()

class KostalFloat32Sensor(KostalSensor):
    """ Kostal FLOAT32 sensor."""

    def __init__(self, coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class = SensorStateClass.MEASUREMENT):
        super().__init__(coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class)

    @property
    def state(self):
        return self.coordinator.read_float32(self._register_address)




class KostalInt16Sensor(KostalSensor):
    """ Kostal INT16 sensor."""

    def __init__(self, coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class = SensorStateClass.MEASUREMENT):
        super().__init__(coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class)

    @property
    def state(self):
        return self.coordinator.read_int16(self._register_address)


class KostalUInt16Sensor(KostalSensor):
    """ Kostal UINT16 sensor."""

    def __init__(self, coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class = SensorStateClass.MEASUREMENT):
        super().__init__(coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class)

    @property
    def state(self):
        return self.coordinator.read_uint16(self._register_address)
    



class KostalInt32Sensor(KostalSensor):
    """ Kostal INT32 sensor."""

    def __init__(self, coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class = SensorStateClass.MEASUREMENT):
        super().__init__(coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class)

    @property
    def state(self):
        return self.coordinator.read_int32(self._register_address)


class KostalUInt32Sensor(KostalSensor):
    """ Kostal UINT32 sensor."""
    def __init__(self, coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class = SensorStateClass.MEASUREMENT):
        super().__init__(coordinator, ip_address, register_address, unique_id, name, icon, device_class, native_unit_of_measurement, suggested_display_precision, sensor_state_class)

    @property
    def state(self):
        return self.coordinator.read_uint32(self._register_address)
    







class BatteryWorkCapacitySensor(KostalFloat32Sensor):
    """Battery work capacity sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, ip_address, register_address, "battery_work_capacity_sensor", "Battery work capacity", "mdi:battery", "energy_storage", "Wh", 0)



class PowerScaleFactorSensor(KostalInt16Sensor):
    """ Power Scale Factor sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, ip_address, register_address, "power_scale_factor", "Power Scale Factor", "mdi:function-variant", None, None, 0)



class MaxChargePowerSensor(KostalFloat32Sensor):
    """Battery Maximum charge power limit sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, ip_address, register_address, "max_charge_power_sensor", "Maximum Charge Power", "mdi:battery-charging-90", "power", "W", 0)


class MaxDischargePowerSensor(KostalFloat32Sensor):
    """Battery Maximum discharge power limit sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, ip_address, register_address, f"max_discharge_power_sensor", "Maximum Discharge Power", "mdi:battery-charging-10", "power", "W", 0)


class CurrentDcSensor(KostalFloat32Sensor):
    """Current DC sensor."""

    def __init__(self, coordinator, ip_address, dc_number, register_address):
        super().__init__(coordinator, ip_address, register_address, f"current_dc_sensor_{dc_number}", f"Current DC {dc_number}", "mdi:current-dc", "current", "A", 2)


class PowerDcSensor(KostalFloat32Sensor):
    """Power DC sensor."""

    def __init__(self, coordinator, ip_address, dc_number, register_address):
        super().__init__(coordinator, ip_address, register_address, f"power_dc_sensor_{dc_number}", f"Power DC {dc_number}", "mdi:flash", "power", "W", 0)


class VoltageDcSensor(KostalFloat32Sensor):
    """Voltage DC sensor."""

    def __init__(self, coordinator, ip_address, dc_number, register_address):
        super().__init__(coordinator, ip_address, register_address, f"voltage_dc_sensor_{dc_number}", f"Voltage DC {dc_number}", "mdi:sine-wave", "voltage", "V", 0)



class ControllerTemperatureSensor(KostalFloat32Sensor):
    """Temperature of controller PCB sensor."""

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, ip_address, register_address, "controller_temperature_sensor", "Controller Temperature", "mdi:thermometer", "TEMPERATURE", "°C", 1)


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
            "Unknown"
        ]

    def __init__(self, coordinator, ip_address, register_address):
        super().__init__(coordinator, context=0)

        self._ip_address = ip_address  # Initialize the IP address
        self._register_address = register_address
        self._state = None

        self._name = f"Inverter State"
        self._unique_id = f"inverter_state_sensor_{ip_address.replace('.', '_')}"
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
        return list(self._options_enum)