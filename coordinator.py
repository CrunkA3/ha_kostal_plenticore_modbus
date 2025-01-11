"""Coordinators for willow."""
from __future__ import annotations

from datetime import timedelta
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.const import PERCENTAGE

from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_IP_ADDRESS, NAME, MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)

class InverterCoordinator(DataUpdateCoordinator):
    """Inverter coordinator.

    The CoordinatorEntity class provides:
        should_poll
        async_update
        async_added_to_hass
        available
    """


    def __init__(self, hass, entry, ip_address):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=15),
        )

        self._hass = hass
        self._entry = entry
        self._ip_address = ip_address

        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN].setdefault(entry.entry_id, {
                    "name": entry.title,
                    "ip": ip_address,
                    "model": MODEL,
                    "status": "OFFLINE"
                })

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {
                (DOMAIN, self._entry.entry_id)
                },
            "name": NAME,
            "manufacturer": MANUFACTURER,
            "model": MODEL
        }

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        client = AsyncModbusTcpClient(self._ip_address, port=1502)  # IP-Adresse und Port des Inverters

        data = { 
            "scaleFactor": 1,
            "batteryWorkCapacity": 0,
            "maxChargePower": 0,
            "maxDischargePower": 0,
            "min_soc": 5,
            "max_soc": 100
        }


        try:
            connection = await client.connect()
            if connection:

                # Power Scale Factor
                result = await client.read_holding_registers(1025, count=1, slave=71)
                if not result.isError():
                    #result_float = client.convert_from_registers(registers=result.registers, data_type=client.DATATYPE.FLOAT32, word_order="little")
                    power_scale_factor = client.convert_from_registers(registers=result.registers, data_type=client.DATATYPE.INT16)
                    data["scaleFactor"] = power_scale_factor
                else:
                    _LOGGER.error("Error reading registers")

                # batteryWorkCapacity
                result = await client.read_holding_registers(1068, count=2, slave=71)
                if not result.isError():
                    result_float = client.convert_from_registers(registers=list(reversed(result.registers)), data_type=client.DATATYPE.FLOAT32)
                    data["batteryWorkCapacity"] = result_float
                else:
                    _LOGGER.error("Error reading registers")

                # Battery max. charge/discharge power limit and Minimum/Maximum SOC
                result = await client.read_holding_registers(1038, count=8, slave=71)
                if not result.isError():
                    max_charge_power_limit = client.convert_from_registers(registers=list(reversed(result.registers[:2])), data_type=client.DATATYPE.FLOAT32)
                    max_discharge_power_limit = client.convert_from_registers(registers=list(reversed(result.registers[2:4])), data_type=client.DATATYPE.FLOAT32)
                    min_soc = client.convert_from_registers(registers=list(reversed(result.registers[4:6])), data_type=client.DATATYPE.FLOAT32)
                    max_soc = client.convert_from_registers(registers=list(reversed(result.registers[6:8])), data_type=client.DATATYPE.FLOAT32)

                    data["maxChargePower"] = max_charge_power_limit
                    data["maxDischargePower"] = max_discharge_power_limit
                    data["min_soc"] = min_soc
                    data["max_soc"] = max_soc
                else:
                    _LOGGER.error("Error reading registers")
            else:
                _LOGGER.error("Connection failed")

        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")

        finally:
            client.close()

        return data

    async def async_set_min_soc(self, value: float) -> None:
        """set minimum soc"""        
        _LOGGER.warn("InverterCoordinator async_set_min_soc")

        client = AsyncModbusTcpClient(self._ip_address, port=1502)  # IP-Adresse und Port des Inverters

        try:
            connection = await client.connect()
            if connection:

                registers = client.convert_to_registers(value=value, data_type=client.DATATYPE.FLOAT32)
                result = await client.write_registers(1042, values=list(reversed(registers)), slave=71)
                if not result.isError():
                    _LOGGER.error("Error writing registers")

            else:
                _LOGGER.error("Connection failed")

        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")

        finally:
            client.close()

    async def async_set_float_alue(self, address: int, value: float) -> None:
        """Set Float Value"""
        
        client = AsyncModbusTcpClient(self._ip_address, port=1502)  # IP-Adresse und Port des Inverters

        try:
            connection = await client.connect()
            if connection:

                registers = client.convert_to_registers(value=value, data_type=client.DATATYPE.FLOAT32)
                result = await client.write_registers(1042, values=list(reversed(registers)), slave=71)
                if not result.isError():
                    _LOGGER.error("Error writing registers")

            else:
                _LOGGER.error("Connection failed")

        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")

        finally:
            client.close()

