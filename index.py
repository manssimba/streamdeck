#!/usr/bin/env python3

#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Example script showing basic library usage - updating key images with new
# tiles generated at runtime, and responding to button state change events.

import os
import threading
import time
from soco import SoCo
my_zone = SoCo('192.168.68.129')
sonosConnected = False

#try and see if sonos is connected
try:
    print(my_zone.player_name)
    print("Sonos is connected")
    sonosConnected = True
except:
    print("Sonos is not connected")

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

display = "home"

#create an array of 5 player names
players = ["home", "sonos"]
playersCurrent = 0
running = False


def render_key_image_from_array(deck, font_filename, array):
    #step 1: create an empty image
    image = Image.new("RGBA", (64, 64))
    #step 2: use image to create scaled key image
    image = PILHelper.create_scaled_key_image(deck, image, margins=[0, 0, 0, 0])

    #step 3: load a custom TrueType font and use it to overlay the key index, draw 3 lines of text onto the image, one in the middle thats brighter, and one at the top and bottom thats darker
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 18)
    currentKey = playersCurrent
    draw.text((image.width / 2, 39), text=array[currentKey], font=font, anchor="ms", fill="white")
    currentKey = currentKey - 1
    #make sure that currentKey doesn't go below 0 or above the length of the array
    if currentKey < 0:
        currentKey = len(array) - 1
    if currentKey > len(array) - 1:
        currentKey = 0
    draw.text((image.width / 2, 19), text=array[currentKey], font=font, anchor="ms", fill="gray")
    currentKey = playersCurrent + 1
    print(currentKey)
    print(playersCurrent)
    if currentKey < 0:
        currentKey = len(array) - 1
    if currentKey > len(array) - 1:
        currentKey = currentKey = 0
    draw.text((image.width / 2, 59), text=array[currentKey], font=font, anchor="ms", fill="gray")

    return PILHelper.to_native_key_format(deck, image)

# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.

    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_key_image(deck, icon, margins=[0, 0, 0, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 18)
    draw.text((image.width / 2, 19), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_key_format(deck, image)


# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    name = "undefined"
    icon = "undefined"

    #multiple displays: home, exit (to ask if user wants to exit)
    if display != "exit":
        exit_key_index = deck.key_count() - 1

        if key == exit_key_index:
            name = "exit"
            icon = "{}.png".format("streamdeck/vehicle-exit")
            font = "Arial.ttf"
            label = ""

        elif key == 0:
            name = "up"
            icon = "{}.png".format("streamdeck/vehicle-arrow-up" if state else "streamdeck/settings-arrow-up")
            font = "Arial.ttf"
            label = ""
        
        elif key == 5:
            name = "down"
            icon = "{}.png".format("streamdeck/vehicle-arrow-down" if state else "streamdeck/settings-arrow-down")
            font = "Arial.ttf"
            label = ""

        elif key == 10:
            name = "select"
            #icon = "".format("streamdeck/vehicle-ok" if state else "streamdeck/settings-ok")
            font = "Arial.ttf"
            label = "Thingy"
        elif key == 4:
            name = "play"
            icon = "{}.png".format("streamdeck/music-music-pause" if running else "streamdeck/music-music-play")
            font = "Arial.ttf"
            label = ""
        elif key == 9:
            name = "repeat"
            icon = "{}.png".format("streamdeck/music-music-repeat-all")
            font = "Arial.ttf"
            label = ""
    







    
    if display == "sonos":
        if key == 7 and sonosConnected:
            print("sonos updated")
            if my_zone.get_current_transport_info()['current_transport_state'] == "PLAYING":
                name = "sonosPause"
                icon = "{}.png".format("streamdeck/music-music-pause")
                font = "Arial.ttf"
                label = ""
            else:
                name = "sonosPlay"
                icon = "{}.png".format("streamdeck/music-music-play")
                font = "Arial.ttf"
                label = ""

        elif key == 6 and sonosConnected:
            name = "sonosPrevious"
            icon = "{}.png".format("streamdeck/music-music-prev")
            font = "Arial.ttf"
            label = ""

        elif key == 8 and sonosConnected:
            name = "sonosNext"
            icon = "{}.png".format("streamdeck/music-music-next")
            font = "Arial.ttf"
            label = ""
        elif key == 12 and sonosConnected:
            name = "sonosVolumeDown"
            icon = "{}.png".format("streamdeck/music-music-volume-down")
            font = "Arial.ttf"
            label = ""

        elif key == 2 and sonosConnected:
            name = "sonosVolumeUp"
            icon = "{}.png".format("streamdeck/music-music-volume-up")
            font = "Arial.ttf"
            label = ""
    elif display == "exit":
        if key == 6:
            name = "exitConfirm"
            icon = "{}.png".format("streamdeck/vehicle-exit")
            font = "Arial.ttf"
            label = ""
        elif key == 8:
            name = "exitCancel"
            icon = "{}.png".format("streamdeck/settings-cancel")
            font = "Arial.ttf"
            label = ""
        elif key == 2:
            name = "restartConfirm"
            icon = "{}.png".format("streamdeck/settings-restart")
            font = "Arial.ttf"
            label = ""
        else:
            name = "empty"
            icon = "{}.png".format("Released")
            font = "Arial.ttf"
            label = ""

    if name == "undefined":
            name = "empty"
            icon = "{}.png".format("Released")
            font = "Arial.ttf"
            label = ""


    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }

# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    if key_style["icon"] == os.path.join(ASSETS_PATH, "undefined"):
        image = render_key_image_from_array(deck, key_style["font"], players)

    # Generate the custom key with the requested image and label.
    else:
        image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)


# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Don't try to draw an image on a touch button
    if key >= deck.key_count():
        return

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)
        global display
        global playersCurrent
        global running
        # When an exit button is pressed, close the application.
        if key_style["name"] == "exitConfirm":
            # Use a scoped-with on the deck to ensure we're the only thread
            # using it right now.
            with deck:
                # Reset deck, clearing all button images.
                deck.reset()

                # Close deck handle, terminating internal worker threads.
                deck.close()

        if key_style["name"] == "exit":
            #change display to exit
            display = "exit"
            #rerender all keys
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)
        
        if key_style["name"] == "exitCancel":
            #change display to exit
 
            display = "home"
            #rerender all keys
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)
        
        if key_style["name"] == "restartConfirm":
            with deck:
                deck.reset()
                deck.close()
                #run the py file again
                os.system("python index.py")
        
        if key_style["name"] == "down":
            playersCurrent = playersCurrent + 1
            #check if playersCurrent is greater than the length of the array
            if playersCurrent > len(players) - 1:
                playersCurrent = 0
            #rerender all keys
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)
        
        if key_style["name"] == "up":
            playersCurrent = playersCurrent - 1
            #check if playersCurrent is less than 0
            if playersCurrent < 0:
                playersCurrent = len(players) - 1
            #rerender all keys
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)
        
        if key_style["name"] == "play":
            running = not running
            #rerender this key
            update_key_image(deck, key, running)
        
        if key_style["name"] == "sonosPause":
            my_zone.pause()
        
        if key_style["name"] == "sonosPlay":
            #update key after playing has resumed (takes around one second)
            my_zone.play()
            #loop until sonos is playing
            while my_zone.get_current_transport_info()['current_transport_state'] != "PLAYING":
                time.sleep(0.10)
                print("checking")
            #rerender this key
            update_key_image(deck, key, False)


        if key_style["name"] == "sonosNext":
            my_zone.next()
        
        if key_style["name"] == "sonosPrevious":
            my_zone.previous()

        if key_style["name"] == "sonosVolumeUp":
            my_zone.volume += 2
        
        if key_style["name"] == "sonosVolumeDown":
            my_zone.volume -= 2

        if key_style["name"] == "select":
            #change display to value of players

            display = players[playersCurrent]

            print(display)
            #rerender all keys
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)




if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)



        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass
