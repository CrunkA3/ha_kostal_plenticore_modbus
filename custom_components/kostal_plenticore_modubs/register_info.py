from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)

class RegisterInfo():
    """Register Information"""

    def __init__(self, address, unique_id, name, unit, type, icon, device_class, display_precision, access = "RO", sensor_state_class = SensorStateClass.MEASUREMENT):
        """
        Initialize a new RegisterInfo object.

        Args:
            address (str): register address
            unique_id (str): unique id
            name (str): register name
            unit (str): data unit
            type (str): data type
            icon (str): data type
            device_class (str): data type
            display_precision (str): Display precision
            access (int, optional): Acces mode
        """
        self._address = address
        self._unique_id = unique_id
        self._name = name
        self._unit = unit
        self._type = type
        self._type = type
        self._icon = icon
        self._device_class = device_class
        self._display_precision = display_precision
        self._access = access
        self._sensor_state_class = sensor_state_class

    # Getter for address
    @property
    def address(self):
        return self._address

    # Getter for unique_id
    @property
    def unique_id(self):
        return self._unique_id

    # Getter for name
    @property
    def name(self):
        return self._name

    # Getter for unit
    @property
    def unit(self):
        return self._unit

    @property
    def type(self):
        """Getter for type"""
        return self._type

    # Getter for icon
    @property
    def icon(self):
        """Getter for icon"""
        return self._icon

    # Getter for device_class
    @property
    def device_class(self):
        """Getter for device_class"""
        return self._device_class

    # Getter for display_precision
    @property
    def display_precision(self):
        return self._display_precision

    # Getter for access
    @property
    def access(self):
        return self._access

    @property
    def sensor_state_class(self):
        """Getter for sensor_state_class"""
        return self._sensor_state_class


REGISTERS: list[RegisterInfo] = [
    RegisterInfo(514, "battery_actual_soc", "Battery actual SOC", "%", "U16", "mdi:battery", "BATTERY", 0),
    RegisterInfo(106, "consumption_battery", "Home own consumption from battery", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(108, "consumption_grid", "Home own consumption from grid", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(116, "consumption_pv", "Home own consumption from PV", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(110, "consumption_battery_total", " Total home consumption Battery", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(112, "consumption_grid_total", " Total home consumption Grid", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(114, "consumption_pv_total", " Total home consumption PV", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(118, "consumption_total", "Total home consumption", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(118, "worktime", "Worktime", "s", "Float", "mdi:timer", "duration", 0, SensorStateClass.TOTAL),
    RegisterInfo(194, "number_battery_cycles", "Number of battery cycles", None, "Float", "mdi:counter", None, 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(214, "battery_temperature", "Battery temperature", "°C", "Float", "mdi:thermometer", "TEMPERATURE", 1)
]