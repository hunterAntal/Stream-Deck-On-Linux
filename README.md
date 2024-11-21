# Stream Deck Volume Control

A Python application that allows you to control the volume of a specified application (e.g., Spotify) on a Linux system using an Elgato Stream Deck. It maps Stream Deck buttons to volume up, volume down, and mute/unmute actions for the target application.

## Features

- **Volume Up**: Increase the volume of the target application by a fixed percentage.
- **Volume Down**: Decrease the volume of the target application by a fixed percentage.
- **Mute/Unmute**: Toggle mute status for the target application.
- **Dynamic Button Icons**: Updates the Stream Deck button icons to reflect the current volume state.

## Requirements

### Operating System

- Linux (Tested on Linux Mint)

### Python

- Version: 3.x
- Libraries:
  - `streamdeck`
  - `Pillow`
  - `hidapi`

### System Dependencies

- `pactl` (PulseAudio control utility)
- `libhidapi-hidraw0` and `libhidapi-libusb0` (for HID API)
- `libusb-1.0-0-dev`

### Running
Running the lsusb | grep Elgato command will list any connected Elgato devices recognized by the system. If your Stream Deck is plugged in and properly detected


Activate the Virtual Environment:
    source env/bin/activate
deactivate:
    deactivate

Run StreamDeck:
    python3 streamdeckVolumeControl.py

