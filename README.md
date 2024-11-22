# Stream Deck Volume Control

A Python application that allows you to control the volume of a specified application (e.g., Spotify) on a Linux system using an Elgato Stream Deck. It maps Stream Deck buttons to volume up, volume down, and mute/unmute actions for the target application.

## Features

- **Volume Up**: Increase the volume of the target application by a fixed percentage.
- **Volume Down**: Decrease the volume of the target application by a fixed percentage.
- **Mute/Unmute**: Toggle mute status for the target application.
- **Play/Pause**
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
- 'playerctl' (for controlling media playback)

### Running
Running the lsusb | grep Elgato command will list any connected Elgato devices recognized by the system. If your Stream Deck is plugged in and properly detected

### Steps
1. Go to folder you saved the files to in Terminal
2. Start up a python enviornment
- python3 -m venv env
- source env/bin/activate
3. Install Python Dependencies
- pip install streamdeck Pillow hidapi
4. Install System Dependencies
- sudo apt-get install pulseaudio-utils libhidapi-hidraw0 libhidapi-libusb0 libusb-1.0-0-dev
5. Set Up udev Rules for Stream Deck Access
- Create a udev rules file to allow non-root access to the Stream Deck:
- sudo nano /etc/udev/rules.d/99-streamdeck.rules
- Add the following content (replace YOUR_PRODUCT_ID with your Stream Deck's product ID):
- SUBSYSTEM=="input", GROUP="input", MODE="0666"
- KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", MODE="0666", GROUP="plugdev"
-KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="YOUR_PRODUCT_ID", MODE="0666", GROUP="plugdev"

Note: You can find your Stream Deck's product ID by running lsusb and looking for the Elgato device.
- Reload udev rules and replug the device:
- sudo udevadm control --reload-rules
- sudo udevadm trigger
6. Add User to plugdev Group
- sudo usermod -aG plugdev $USER
- Log out and log back in to apply group changes.
7. python3 streamdeckVolumeControl.py

Press the buttons on your Stream Deck:

- Button 0: Volume Down
- Button 1: Volume Up
- Button 2: Mute/Unmute


Activate the Virtual Environment:
    source env/bin/activate
deactivate:
    deactivate

Run StreamDeck:
    python3 streamdeckVolumeControl.py

