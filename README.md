# Stream-Deck-On-Linux
Stream Deck Volume Control
A Python application that allows you to control the volume of a specified application (e.g., Spotify) on a Linux system using an Elgato Stream Deck. It maps Stream Deck buttons to volume up, volume down, and mute/unmute actions for the target application.

Features
Volume Up: Increase the volume of the target application by a fixed percentage.
Volume Down: Decrease the volume of the target application by a fixed percentage.
Mute/Unmute: Toggle mute status for the target application.
Dynamic Button Icons: Updates the Stream Deck button icons to reflect the current volume state.
Requirements
Operating System: Linux (Tested on Linux Mint)
Python: 3.x
Python Libraries:
streamdeck
Pillow
hidapi
System Dependencies:
pactl (PulseAudio control utility)
libhidapi-hidraw0 and libhidapi-libusb0 (for HID API)
libusb-1.0-0-dev
Installation
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/streamdeck-volume-control.git
cd streamdeck-volume-control
Set Up Virtual Environment (Optional but Recommended)

bash
Copy code
python3 -m venv env
source env/bin/activate
Install Python Dependencies

bash
Copy code
pip install streamdeck Pillow hidapi
Install System Dependencies

bash
Copy code
sudo apt-get install pulseaudio-utils libhidapi-hidraw0 libhidapi-libusb0 libusb-1.0-0-dev
Set Up udev Rules for Stream Deck Access

Create a udev rules file to allow non-root access to the Stream Deck:

bash
Copy code
sudo nano /etc/udev/rules.d/99-streamdeck.rules
Add the following content (replace YOUR_PRODUCT_ID with your Stream Deck's product ID):

plaintext
Copy code
SUBSYSTEM=="input", GROUP="input", MODE="0666"
KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", MODE="0666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="YOUR_PRODUCT_ID", MODE="0666", GROUP="plugdev"
Note: You can find your Stream Deck's product ID by running lsusb and looking for the Elgato device.

Reload udev rules and replug the device:

bash
Copy code
sudo udevadm control --reload-rules
sudo udevadm trigger
Add User to plugdev Group

bash
Copy code
sudo usermod -aG plugdev $USER
Log out and log back in to apply group changes.

Prepare Icon Images

Create an icons directory in the project root.
Add the following icon images to the icons directory:
vol_down.png: Icon representing volume down.
vol_up.png: Icon representing volume up.
muted.png: Icon representing the muted state.
unmuted.png: Icon representing the unmuted state.
Note: Ensure these images are appropriately sized for your Stream Deck model (typically 72x72 or 80x80 pixels).

Configuration
Target Application

The script controls the volume of the application specified by the TARGET_APP variable in streamdeckVolumeControl.py. By default, it's set to spotify. You can change it to any application that appears in pactl list sink-inputs.

python
Copy code
TARGET_APP = "spotify"
Volume Step Size

Adjust the volume increment/decrement percentage in the increase_volume() and decrease_volume() functions:

python
Copy code
subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '+5%'])
subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '-5%'])
Font Path

Ensure the font path in the render_key_image() function points to a valid font on your system:

python
Copy code
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
You can find available fonts using:

bash
Copy code
fc-list | grep .ttf
Usage
Run the script:

bash
Copy code
python3 streamdeckVolumeControl.py
Press the buttons on your Stream Deck:

Button 0: Volume Down
Button 1: Volume Up
Button 2: Mute/Unmute
The icons on the Stream Deck will update to reflect the current volume state.

Troubleshooting
Stream Deck Not Found

Ensure the Stream Deck is connected and udev rules are correctly set up.

Permissions Error

If you receive a permissions error, make sure your user is in the plugdev group and that udev rules are correctly configured.

Font Not Found

If you encounter an error related to fonts, update the font_path variable to point to a font available on your system.

Target Application Not Found

If the script reports that the target application is not running, ensure the application is open and that TARGET_APP matches the application's name in pactl list sink-inputs.

Icons Not Displaying Correctly

Verify that the icon files are in the correct directory and named properly.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Based on the Stream Deck library and examples.
Inspired by the need to control application volume via hardware buttons.
Thanks to the open-source community for providing the tools and libraries used in this project.