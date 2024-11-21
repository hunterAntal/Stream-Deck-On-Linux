import sys
import threading
import logging
import subprocess
from time import sleep
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
VOLUME_DOWN_BUTTON = 0
VOLUME_UP_BUTTON = 1
MUTE_TOGGLE_BUTTON = 2
PLAY_PAUSE_BUTTON = 3  # New button for play/pause
TARGET_APP = "spotify"

# Function to get the sink input ID of the target application
def get_sink_input_id():
    result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE)
    output = result.stdout.decode()

    sink_inputs = output.split('Sink Input #')
    for sink in sink_inputs:
        if TARGET_APP.lower() in sink.lower():
            sink_id_line = sink.strip().split('\n')[0]
            sink_id = sink_id_line.strip()
            logging.info(f"Found {TARGET_APP} with Sink Input ID: {sink_id}")
            return sink_id
    logging.error(f"{TARGET_APP} is not running.")
    return None

def increase_volume():
    sink_id = get_sink_input_id()
    if sink_id:
        subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '+5%'])

def decrease_volume():
    sink_id = get_sink_input_id()
    if sink_id:
        subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '-5%'])

def toggle_mute():
    sink_id = get_sink_input_id()
    if sink_id:
        subprocess.run(['pactl', 'set-sink-input-mute', sink_id, 'toggle'])

def get_current_volume():
    sink_id = get_sink_input_id()
    if sink_id:
        result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        sink_info = output.split(f'Sink Input #{sink_id}')[1]
        volume_lines = [line for line in sink_info.split('\n') if 'Volume:' in line and '%' in line]
        if volume_lines:
            volume_line = volume_lines[0]
            # Extract the percentage value
            volume_percent = volume_line.split('/')[-1].strip()
            return volume_percent
    return None

def toggle_play_pause():
    subprocess.run(['playerctl', '-p', 'spotify', 'play-pause'])

def get_playback_status():
    result = subprocess.run(['playerctl', '-p', 'spotify', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status = result.stdout.decode().strip()
    if status == '':
        return 'Stopped'  # If Spotify is not running
    return status  # 'Playing' or 'Paused'

def is_muted():
    sink_id = get_sink_input_id()
    if sink_id:
        result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        sink_info = output.split(f'Sink Input #{sink_id}')[1]
        mute_lines = [line for line in sink_info.split('\n') if 'Mute:' in line]
        if mute_lines:
            mute_line = mute_lines[0]
            return 'yes' in mute_line
    return False

# Function to render key images
def render_key_image(deck, icon_filename, label):
    # Create new key image of the correct dimensions
    image = PILHelper.create_image(deck)
    draw = ImageDraw.Draw(image)

    # Load the icon image
    icon = Image.open(icon_filename)
    icon = icon.resize((image.width, image.height))
    image.paste(icon, (0, 0))

    # Draw the label
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update the font path if necessary
    font = ImageFont.truetype(font_path, 14)
    draw.text((image.width / 2, image.height - 20), text=label, font=font, anchor="ms", fill="white")

    # Convert the PIL image to a format native to the device
    return PILHelper.to_native_format(deck, image)

# Function to update the key images
def update_key_images(deck):
    # Volume Down Button
    vol_down_image = render_key_image(deck, "icons/vol_down.png", "Vol Down")
    deck.set_key_image(VOLUME_DOWN_BUTTON, vol_down_image)

    # Volume Up Button
    vol_up_image = render_key_image(deck, "icons/vol_up.png", "Vol Up")
    deck.set_key_image(VOLUME_UP_BUTTON, vol_up_image)

    # Mute/Unmute Button
    mute_status = "Muted" if is_muted() else "Unmuted"
    mute_icon = "icons/unmuted.png" if is_muted() else "icons/muted.png"
    mute_image = render_key_image(deck, mute_icon, mute_status)
    deck.set_key_image(MUTE_TOGGLE_BUTTON, mute_image)

    # Play/Pause Button
    playback_status = get_playback_status()
    if playback_status == 'Playing':
        play_pause_icon = "icons/pause.png"
        play_pause_label = "Pause"
    else:
        play_pause_icon = "icons/play.png"
        play_pause_label = "Play"

    play_pause_image = render_key_image(deck, play_pause_icon, play_pause_label)
    deck.set_key_image(PLAY_PAUSE_BUTTON, play_pause_image)

# Key press event handler
def key_change_callback(deck, key, state):
    if state:  # Key is pressed
        if key == VOLUME_DOWN_BUTTON:
            logging.info("Volume Down button pressed.")
            decrease_volume()
        elif key == VOLUME_UP_BUTTON:
            logging.info("Volume Up button pressed.")
            increase_volume()
        elif key == MUTE_TOGGLE_BUTTON:
            logging.info("Mute/Unmute button pressed.")
            toggle_mute()

        elif key == PLAY_PAUSE_BUTTON:
            logging.info("Play/Pause button pressed.")
            toggle_play_pause()

        update_key_images(deck)

# Main function
def main():
    # Discover connected Stream Deck devices
    streamdecks = DeviceManager().enumerate()

    if not streamdecks:
        logging.error("No Stream Deck devices found.")
        sys.exit()

    # Use the first Stream Deck device
    deck = streamdecks[0]
    deck.open()
    deck.reset()

    # Set initial key images
    update_key_images(deck)

    # Register callback function for key press events
    deck.set_key_callback(key_change_callback)

    try:
        # Keep the application running
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        deck.reset()
        deck.close()

if __name__ == "__main__":
    main()
