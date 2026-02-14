"""Coordinators for willow."""
from __future__ import annotations

from datetime import timedelta
from typing import Final
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

        # Optimized read plan (<=125 regs each). Covers:
        # - inverter_state (56..57) + all sensors/numbers used by this integration incl. modbus_wichtig.xlsx set

        READ_BLOCKS: Final[list[tuple[int, int]]] = [
                (56, 2),  # inverter state (uint32 via word-swap)
                (98, 22),  # 98..119  (controller temp + consumption/power/energy around 100..118)
                (144, 2),  # worktime
                (156, 18),  # 156..173  (AC power phases)
                (194, 94),  # 194..287  (battery/house/grid + DC currents/powers/voltages)
                (320, 8),  # 320..327  (yields)
                (512, 18),  # 512..529  (battery SOC etc.)
                (1024, 8),  # 1024..1031 (charge setpoint + scale factor + charge power number @1030)
                (1042, 38),  # 1042..1079 (min/max soc + totals + battery work cap + max ch/disch)
        ]

        async def read_holding_registers(address, count):
            result = await client.read_holding_registers(address, count=count, device_id=71)
            if not result.isError():
                data["registers"][address:address+count] = result.registers
            else:
                _LOGGER.error("Error reading registers: addr=%s count=%s", address, count)

        try:
            connection = await client.connect()

            if connection:
                for addr, cnt in READ_BLOCKS:
                    await read_holding_registers(addr, cnt)

                # Inverter state decode from buffered registers (56..57) - word swap for CDAB
                inv_regs = data["registers"][56:58]
                data["inverter_state"] = client.convert_from_registers(
                    registers = list(reversed(inv_regs)),
                    data_type = client.DATATYPE.UINT32
                )

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
