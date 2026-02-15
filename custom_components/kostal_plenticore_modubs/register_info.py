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
        self._icon = icon
        self._device_class = device_class
        self._display_precision = display_precision
        self._access = access
        self._sensor_state_class = sensor_state_class

    # Getter for address
    @property
    def address(self):
        """Getter for address"""
        return self._address

    # Getter for unique_id
    @property
    def unique_id(self):
        """Getter for unique_id"""
        return self._unique_id

    # Getter for name
    @property
    def name(self):
        """Getter for name"""
        return self._name

    # Getter for unit
    @property
    def unit(self):
        """Getter for unit"""
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
        """Getter for display_precision"""
        return self._display_precision

    # Getter for access
    @property
    def access(self):
        """Getter for access"""
        return self._access

    @property
    def sensor_state_class(self):
        """Getter for sensor_state_class"""
        return self._sensor_state_class


REGISTERS: list[RegisterInfo] = [
    RegisterInfo(514, "battery_actual_soc", "Battery actual SOC", "%", "U16", "mdi:battery", "BATTERY", 0),
    RegisterInfo(100, "total_dc_power", "Total DC power", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(106, "consumption_battery", "Home own consumption from battery", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(108, "consumption_grid", "Home own consumption from grid", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(116, "consumption_pv", "Home own consumption from PV", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(110, "consumption_battery_total", " Total home consumption Battery", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(112, "consumption_grid_total", " Total home consumption Grid", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(114, "consumption_pv_total", " Total home consumption PV", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(118, "consumption_total", "Total home consumption", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(118, "worktime", "Worktime", "s", "Float", "mdi:timer", "duration", 0, SensorStateClass.TOTAL),
    RegisterInfo(156, "active_power_phase_1", "Active power Phase 1", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(162, "active_power_phase_2", "Active power Phase 2", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(170, "active_power_phase_3", "Active power Phase 3", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(172, "total_ac_active_power", "Total AC active power", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(194, "number_battery_cycles", "Number of battery cycles", None, "Float", "mdi:counter", None, 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(200, "actual_battery_charge", "Actual battery charge", "A", "Float", "mdi:current-dc", "current", 2),
    RegisterInfo(514, "act_state_of_charge", "Act. state of charge", "%", "Float", "mdi:battery", "BATTERY", 0),
    RegisterInfo(214, "battery_temperature", "Battery temperature", "°C", "Float", "mdi:thermometer", "TEMPERATURE", 1),
    RegisterInfo(216, "battery_voltage", "Battery voltage", "V", "Float", "mdi:sine-wave", "voltage", 0),
    RegisterInfo(224, "active_power_phase_1_powermeter", "Active power phase 1 (powermeter)", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(234, "active_power_phase_2_powermeter", "Active power phase 2 (powermeter)", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(244, "active_power_phase_3_powermeter", "Active power phase 3 (powermeter)", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(252, "total_active_power_powermeter", "Total active power (powermeter)", "W", "Float", "mdi:flash", "power", 0),
    RegisterInfo(320, "total_yield", " Total yield", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(322, "daily_yield", " Daily yield", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(324, "yearly_yield", " Yearly yield", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(326, "monthly_yield", " Monthly yield", "Wh", "Float", "mdi:flash", "energy", 0, SensorStateClass.TOTAL_INCREASING),
    RegisterInfo(1025, "power_scale_factor", "Power Scale Factor", None, "S16", "mdi:function-variant", None, 0),
    RegisterInfo(1068, "battery_work_capacity_sensor", "Battery work capacity", "Wh", "Float", "mdi:battery", "energy_storage", 0),
    RegisterInfo(266, "voltage_dc_sensor_1", "Voltage DC 1", "V", "Float", "mdi:sine-wave", "voltage", 0),
    RegisterInfo(276, "voltage_dc_sensor_2", "Voltage DC 2", "V", "Float", "mdi:sine-wave", "voltage", 0),
    RegisterInfo(286, "voltage_dc_sensor_3", "Voltage DC 3", "V", "Float", "mdi:sine-wave", "voltage", 0),
]
