from __future__ import annotations

from dataclasses import dataclass
import logging
from homeassistant import config_entries, core

from .const import (
    DOMAIN,
    CONF_IP_ADDRESS
)

from .coordinator import (
    InverterCoordinator
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = [ "sensor", "number" ]


@dataclass
class KostalPlenticoreModbusData:
    """Class to support type hinting of ring data collection."""
    inverter_coordinator: InverterCoordinator



async def async_setup(hass: core.HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    hass.data[DOMAIN][entry.entry_id] = {}
    _LOGGER.info(f"Setting up {DOMAIN} with {entry.data}")

    ip_address = entry.data[CONF_IP_ADDRESS]
    inverter_coordinator = InverterCoordinator(hass, entry, ip_address)

    await inverter_coordinator.async_config_entry_first_refresh()
    entry.runtime_data = KostalPlenticoreModbusData(
        inverter_coordinator = inverter_coordinator
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
