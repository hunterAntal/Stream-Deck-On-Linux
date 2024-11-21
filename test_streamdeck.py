from StreamDeck.DeviceManager import DeviceManager
import sys

streamdecks = DeviceManager().enumerate()
if not streamdecks:
    print("No Stream Deck devices found.")
    sys.exit()

deck = streamdecks[0]
deck.open()
print("Successfully opened the Stream Deck.")
deck.close()
