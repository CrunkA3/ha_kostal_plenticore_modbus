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
            "inverter_state": 18,
            "registers": [0 for _ in range(1083)]
        }


        try:
            connection = await client.connect()
            if connection:
                # read Registers
                result = await client.read_holding_registers(98, count=8, device_id=71)
                if not result.isError():
                    data["registers"][98:116] = result.registers
                else:
                    _LOGGER.error("Error reading registers")

                # read Registers (Consumption)
                result = await client.read_holding_registers(106, count=14, device_id=71)
                if not result.isError():
                    data["registers"][106:120] = result.registers
                else:
                    _LOGGER.error("Error reading registers")


                # read Registers (Consumption)
                result = await client.read_holding_registers(258, count=30, device_id=71)
                if not result.isError():
                    data["registers"][258:288] = result.registers
                else:
                    _LOGGER.error("Error reading registers")

                # read Registers (Battery)
                result = await client.read_holding_registers(512, count=18, device_id=71)
                if not result.isError():
                    data["registers"][512:530] = result.registers
                else:
                    _LOGGER.error("Error reading registers")

                # read Registers (Power Scale Factor)
                result = await client.read_holding_registers(1025, count=1, device_id=71)
                if not result.isError():
                    data["registers"][1025:1026] = result.registers
                else:
                    _LOGGER.error("Error reading registers")

                # read Registers (Battery max. charge/discharge power limit and Minimum/Maximum SOC)
                result = await client.read_holding_registers(1030, count=53, device_id=71)
                if not result.isError():
                    data["registers"][1030:1083] = result.registers
                else:
                    _LOGGER.error("Error reading registers")


                # Inverter State
                result = await client.read_holding_registers(56, count=2, device_id=71)
                if not result.isError():
                    result_uint = client.convert_from_registers(registers=list(reversed(result.registers)), data_type=client.DATATYPE.UINT32)
                    data["inverter_state"] = result_uint
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

    async def async_set_float_value(self, address: int, value: float) -> None:
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

    def read_float32(self, address: int) -> float:
        return AsyncModbusTcpClient.convert_from_registers(registers=list(reversed(self.data["registers"][address:address+2])), data_type=AsyncModbusTcpClient.DATATYPE.FLOAT32)

    def read_int16(self, address: int) -> int:
        return AsyncModbusTcpClient.convert_from_registers(registers=list(self.data["registers"][address:address+1]), data_type=AsyncModbusTcpClient.DATATYPE.INT16)

    def read_uint16(self, address: int) -> int:
        return AsyncModbusTcpClient.convert_from_registers(registers=list(self.data["registers"][address:address+1]), data_type=AsyncModbusTcpClient.DATATYPE.UINT16)
