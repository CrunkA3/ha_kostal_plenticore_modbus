# Kostal Plenticore Modbus Integration for Home Assistant

![hacs-validate](https://github.com/CrunkA3/ha_kostal_plenticore_modbus/actions/workflows/hacs-validate.yml/badge.svg)
![HACS Action](https://github.com/CrunkA3/ha_kostal_plenticore_modbus/actions/workflows/validate.yml/badge.svg)
![Release](https://github.com/CrunkA3/ha_kostal_plenticore_modbus/actions/workflows/release.yml/badge.svg)

<img alt="screenshot of integration" src="https://github.com/CrunkA3/ha_kostal_plenticore_modbus/blob/main/assets/Example.png" />

## Installation

### Manual Installation

1. **Download the Integration**: Download the integration files from the GitHub repository.
2. **Add to Custom Components**: Place the downloaded files in the `custom_components/ha_kostal_plenticore_modbus` directory within your Home Assistant configuration directory.
3. **Configure Home Assistant**: Add the Kostal Plenticore Modbus integration to your Home Assistant configuration.

### HACS Installation

1. **Open HACS**: Navigate to the Home Assistant Community Store (HACS) in your Home Assistant UI.
2. **Add Custom Repository**: Click on the three dots menu in the top right corner and select "Custom repositories".
3. **Enter Repository URL**: Add the following URL: `https://github.com/CrunkA3/ha_kostal_plenticore_modbus` and select the category as "Integration".
4. **Install the Integration**: After adding the custom repository, search for "EEVE Mower Willow" in HACS and install it.
5. **Restart Home Assistant**: After installation, restart Home Assistant to apply the changes.

## Configuration

To configure the Kostal Plenticore Modbus integration, follow these steps:

1. **Add the Integration**: Go to the Home Assistant UI and navigate to `Configuration` > `Integrations`. Click on the `+` button to add a new integration and search for "Kostal Plenticore Modbus".
2. **Enter IP Address**: Enter the IP address of your Inverter.
3. **Save and Restart**: Save the configuration and restart Home Assistant to apply the changes.

## Available Sensors

This integration provides the following sensors:

### Inverter Status
- **Inverter State** - Current state of the inverter
- **Controller Temperature** (°C) - Temperature of the controller
- **Worktime** (s) - Total working time

### Power Measurements
- **Total DC power** (W) - Total DC power from solar panels
- **Total AC active power** (W) - Total AC active power output
- **Active power Phase 1** (W) - AC power on phase 1
- **Active power Phase 2** (W) - AC power on phase 2
- **Active power Phase 3** (W) - AC power on phase 3

### Home Consumption
- **Home own consumption from battery** (W) - Current consumption from battery
- **Home own consumption from grid** (W) - Current consumption from grid
- **Home own consumption from PV** (W) - Current consumption from solar
- **Total home consumption Battery** (Wh) - Total energy consumed from battery
- **Total home consumption Grid** (Wh) - Total energy consumed from grid
- **Total home consumption PV** (Wh) - Total energy consumed from solar
- **Total home consumption** (Wh) - Total energy consumed

### Battery Information
- **Number of battery cycles** - Battery cycle count
- **Actual battery charge** (A) - Current battery charge
- **Act. state of charge** (%) - Current battery state of charge
- **Battery actual SOC** (%) - Battery actual state of charge
- **Battery Temperature** (°C) - Battery temperature
- **Battery voltage** (V) - Battery voltage
- **Battery work capacity** (Wh) - Battery work capacity
- **Maximum Charge Power** (W) - Maximum charge power
- **Maximum Discharge Power** (W) - Maximum discharge power

### Power Meter
- **Active power phase 1 (powermeter)** (W) - Phase 1 power meter reading
- **Active power phase 2 (powermeter)** (W) - Phase 2 power meter reading
- **Active power phase 3 (powermeter)** (W) - Phase 3 power meter reading
- **Total active power (powermeter)** (W) - Total power meter reading

### DC Sensors (String 1)
- **Current DC 1** (A) - DC current from string 1
- **Power DC 1** (W) - DC power from string 1
- **Voltage DC 1** (V) - DC voltage from string 1

### DC Sensors (String 2)
- **Current DC 2** (A) - DC current from string 2
- **Power DC 2** (W) - DC power from string 2
- **Voltage DC 2** (V) - DC voltage from string 2

### DC Sensors (String 3)
- **Current DC 3** (A) - DC current from string 3
- **Power DC 3** (W) - DC power from string 3
- **Voltage DC 3** (V) - DC voltage from string 3

### Energy Totals
- **Total yield** (Wh) - Total energy produced
- **Daily yield** (Wh) - Energy produced today
- **Yearly yield** (Wh) - Energy produced this year
- **Monthly yield** (Wh) - Energy produced this month
- **Total DC charge energy (DC-side to battery)** (Wh) - Total DC energy charged to battery
- **Total DC discharge energy (DC-side from battery)** (Wh) - Total DC energy discharged from battery
- **Total AC charge energy (AC-side to battery)** (Wh) - Total AC energy charged to battery
- **Total AC discharge energy (battery to grid)** (Wh) - Total energy discharged from battery to grid
- **Total AC charge energy (grid to battery)** (Wh) - Total energy charged from grid to battery
- **Total DC PV energy (sum of all PV inputs)** (Wh) - Total solar energy from all strings
- **Total DC energy from PV1** (Wh) - Total energy from string 1
- **Total DC energy from PV2** (Wh) - Total energy from string 2
- **Total DC energy from PV3** (Wh) - Total energy from string 3
- **Total energy AC-side to grid** (Wh) - Total energy exported to grid
- **Total DC power (sum of all PV inputs)** (W) - Total DC power from all strings
- **Total Real Energy Exported** (Wh) - Total real energy exported
- **Total Real Energy Imported** (Wh) - Total real energy imported

### Other
- **Power Scale Factor** - Power scaling factor
