# Kasa Bridge

Reads the E-meter data from a TP-Link Smart Plug, then sends to InfluxDB over UDP.

By default, it retrieves and sends data every 10 s.

## Requirements

* Python 3
  * asyncio
  * python-kasa

## Usage

1. Set your IP addresses and ports in ```config.json```
2. Run `kasa_bridge.py`