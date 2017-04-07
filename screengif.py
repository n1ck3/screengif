#!/usr/bin/env python

import os
import sys
import subprocess
import time
import datetime
from PIL import Image, ImageGrab

# Constants in seconds
GRAB_INTERVAL=0.1
DURATION=1

def grab_screen(interval, duration):
    """
    Grab the screen at a certain GRAB_INTERVAL.
    """
    images = []
    for i in range(int(duration/interval)):
        images.append(ImageGrab.grab())
        time.sleep(interval)
    return images

def save_gif(images):
    """
    Save the images as an animated .gif to the Desktop
    names: "Screen Gif YYYY-MM-DD at HH.MM.SS.gif"
    """
    for im in images:
            im.thumbnail((1200,900), Image.ANTIALIAS)

    filename = "%s/Desktop/Screen Gif %s.gif" % (
        os.environ['HOME'],
        datetime.datetime.now().strftime("%Y-%m-%d at %H.%M.%S")
    )
    images[0].save(filename, optimize=True, save_all=True, append_images=images[1:], duration=GRAB_INTERVAL*1000*2)
    return filename


def save_to_clipboard(filename):
    command = "tell app \"Finder\" to set the clipboard to ( POSIX file \"%s\" )" % filename
    process = subprocess.Popen(["osascript", "-e", command], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.communicate()

def main():
    """
    Doesn't do anything in itself. Just runs all the
    other functions in the right order.
    """

    clipboard = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c" or sys.argv[1] == "--clipboard":
            clipboard = True
        else:
            print "Unrecognized option: %s" % sys.argv[1]
            sys.exit(1)

    images = grab_screen(GRAB_INTERVAL, DURATION)

    filename = save_gif(images)

    if clipboard:
        save_to_clipboard(filename)

if __name__ == "__main__":
    main()
