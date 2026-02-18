"""Coordinators for willow."""

from __future__ import annotations

from datetime import timedelta
import logging
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.helpers.entity import Entity
from homeassistant.const import PERCENTAGE

from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, NAME, MANUFACTURER, MODEL

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
        hass.data[DOMAIN].setdefault(
            entry.entry_id,
            {
                "name": entry.title,
                "ip": ip_address,
                "model": MODEL,
                "status": "OFFLINE",
            },
        )

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": NAME,
            "manufacturer": MANUFACTURER,
            "model": MODEL,
        }

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        client = AsyncModbusTcpClient(
            self._ip_address, port=1502
        )  # IP-Adresse und Port des Inverters

        data = {"inverter_state": 18, "registers": [0 for _ in range(40355)]}

        async def read_holding_registers(address, count):
            result = await client.read_holding_registers(
                address, count=count, device_id=71
            )
            if not result.isError():
                data["registers"][address : address + count] = result.registers
            else:
                _LOGGER.error("Error reading registers: addr=%s count=%s", address, count)

        try:
            connection = await client.connect()

            if connection:
                # read Registers
                await read_holding_registers(98, 124)

                # Powermeter
                await read_holding_registers(220, 38)

                # DC1, DC2, DC3
                await read_holding_registers(258, 30)

                # yield
                await read_holding_registers(320, 8)

                # read Registers (Battery)
                await read_holding_registers(512, 18)

                # read Registers (Power Scale Factor)
                await read_holding_registers(1025, 1)

                # read Registers (Battery max. charge/discharge power limit and Minimum/Maximum SOC)
                await read_holding_registers(1030, 53)

                # total real energy exported/imported
                await read_holding_registers(40346, 2)
                await read_holding_registers(40354, 2)


                # Inverter State
                result = await client.read_holding_registers(56, count=2, device_id=71)
                if not result.isError():
                    result_uint = client.convert_from_registers(
                        registers=list(reversed(result.registers)),
                        data_type=client.DATATYPE.UINT32,
                    )
                    data["inverter_state"] = result_uint
                else:
                    _LOGGER.error("Error reading registers")

            else:
                _LOGGER.error("Connection failed")

        except ModbusException as e:
            _LOGGER.error("Modbus error: %s", e)

        finally:
            client.close()

        return data

    async def async_set_min_soc(self, value: float) -> None:
        """set minimum soc"""
        _LOGGER.warning("InverterCoordinator async_set_min_soc")

        client = AsyncModbusTcpClient(
            self._ip_address, port=1502
        )  # IP-Adresse und Port des Inverters

        try:
            connection = await client.connect()
            if connection:
                registers = client.convert_to_registers(
                    value=value, data_type=client.DATATYPE.FLOAT32
                )
                result = await client.write_registers(
                    1042, values=list(reversed(registers)), slave=71
                )
                if not result.isError():
                    _LOGGER.error("Error writing registers")

            else:
                _LOGGER.error("Connection failed")

        except ModbusException as e:
            _LOGGER.error("Modbus error: %s", e)

        finally:
            client.close()

    async def async_set_float_value(self, address: int, value: float) -> None:
        """Set Float Value"""

        client = AsyncModbusTcpClient(
            self._ip_address, port=1502
        )  # IP-Adresse und Port des Inverters

        try:
            connection = await client.connect()
            if connection:
                registers = client.convert_to_registers(
                    value=value, data_type=client.DATATYPE.FLOAT32
                )
                result = await client.write_registers(
                    address, values=list(reversed(registers)), slave=71
                )
                if not result.isError():
                    _LOGGER.error("Error writing registers")

            else:
                _LOGGER.error("Connection failed")

        except ModbusException as e:
            _LOGGER.error("Modbus error: %s", e, exc_info=True)

        finally:
            client.close()



    def read_float32(self, address: int) -> float:
        """
        Read Float32 value from registers

        :param address: The starting address of the registers
        :type address: int
        :return: The Float32 value read from the registers
        :rtype: float
        """
        return AsyncModbusTcpClient.convert_from_registers(
            registers=list(reversed(self.data["registers"][address : address + 2])),
            data_type=AsyncModbusTcpClient.DATATYPE.FLOAT32,
        )

    def read_int16(self, address: int) -> int:
        """
        Read Int16 value from registers

        :param address: The starting address of the registers
        :type address: int
        :return: The Int16 value read from the registers
        :rtype: int
        """
        return AsyncModbusTcpClient.convert_from_registers(
            registers=list(self.data["registers"][address : address + 1]),
            data_type=AsyncModbusTcpClient.DATATYPE.INT16,
        )

    def read_uint16(self, address: int) -> int:
        """
        Read UInt16 value from registers

        :param address: The starting address of the registers
        :type address: int
        :return: The UInt16 value read from the registers
        :rtype: int
        """
        return AsyncModbusTcpClient.convert_from_registers(
            registers=list(self.data["registers"][address : address + 1]),
            data_type=AsyncModbusTcpClient.DATATYPE.UINT16,
        )


    def read_int32(self, address: int) -> int:
        """
        Read Int32 value from registers

        :param address: The starting address of the registers
        :type address: int
        :return: The Int32 value read from the registers
        :rtype: int
        """
        return AsyncModbusTcpClient.convert_from_registers(
            registers=list(reversed(self.data["registers"][address : address + 2])),
            data_type=AsyncModbusTcpClient.DATATYPE.INT32,
        )

    def read_uint32(self, address: int) -> int:
        """
        Read UInt32 value from registers

        :param address: The starting address of the registers
        :type address: int
        :return: The UInt32 value read from the registers
        :rtype: int
        """
        return AsyncModbusTcpClient.convert_from_registers(
            registers=list(reversed(self.data["registers"][address : address + 2])),
            data_type=AsyncModbusTcpClient.DATATYPE.UINT32,
        )