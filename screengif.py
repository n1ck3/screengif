#!/usr/bin/env python
"""
Screen Gif

Usage:
    screengif.py [-d DURATION] [-i INTERVAL] [-c | --clipboard] [--debug]
    screengif.py -h | --help
    screengif.py -v | --version

Options:
    -h --help                           Show this screen.
    -v --version                        Show version.
    -i INTERVAL --interval=INTERVAL     Specify frame interval in seconds. [default: 0.1]
    -d DURATION --duration=DURATION     Specify the duration of the GIF. [default: 5]
    -c --clipboard                      Copy the GIF to clipboard.
    --debug                             Show debug information.

"""

from docopt import docopt

import os
import sys
import subprocess
import shutil
import time
import datetime
import tempfile
from PIL import Image, ImageGrab

arguments = docopt(__doc__, version="Screen Gif 0.8")

DEBUG = arguments["--debug"]

def grab_screen(interval, duration):
    """
    Grab the screen at a set interval and for a set duration.

    Returns list of images (frames).
    """
    images = []
    for i in range(int(duration/interval)):
        images.append(ImageGrab.grab())
        time.sleep(interval)
    return images

def generate_gif(images, interval):
    """
    Generates the GIF from frames (saves to temporary file).

    Returns temporary file pointer and its absolute path.
    """
    for im in images:
            im.thumbnail((1200,900), Image.ANTIALIAS)

    tmp_fp, tmp_path = tempfile.mkstemp(suffix=".gif")
    images[0].save(tmp_path, optimize=True, save_all=True, append_images=images[1:], duration=interval*1000*2)
    return tmp_fp, tmp_path

def save_gif(tmp_fp, tmp_path):
    """
    Saves the images as an animated .gif to the Desktop
    (just like OS X default screen capture does) named:
    "Screen Gif YYYY-MM-DD at HH.MM.SS.gif".

    Closes the temp_fp file pointer (removing the temporary file).
    """
    filename = "%s/Desktop/Screen Gif %s.gif" % (
        os.environ['HOME'],
        datetime.datetime.now().strftime("%Y-%m-%d at %H.%M.%S")
    )

    if DEBUG: print "Saving file to %s" % filename

    shutil.copyfile(tmp_path, filename)
    os.close(tmp_fp)
    os.remove(tmp_path)


def copy_to_clipboard(tmp_fp, tmp_path):
    """
    Copies file to clipboard.

    Closes the temp_fp file pointer (removing the temporary file).
    """
    if DEBUG: print "Copying file to clipboard"
    command = "tell app \"Finder\" to set the clipboard to ( POSIX file \"%s\" )" % tmp_path
    process = subprocess.Popen(["osascript", "-e", command], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.communicate()
    os.close(tmp_fp)

    # TODO: Figure out a way to copy the file contents to the clipboard
    #       rather than the file on disk. Removing the file clears the
    #       clipboard.
    # os.remove(tmp_path)

def main():
    """
    Handles argument parsing.

    Invokes the other functions.
    """

    if DEBUG:
        print "Printing debug information."
        print "Arguments:"
        print arguments
        print

    errors = []

    # Handle argument: interval
    try:
        interval = float(arguments["--interval"])
        interval_min = 0.1
        interval_max = 1
        if interval < interval_min or interval > interval_max:
            errors.append(
                "Interval has to be between %s and %s." % (
                    interval_min,
                    interval_max
                )
            )
    except ValueError:
        errors.append("Interval has to be an int of a float.")

    # Handle argument: duration
    try:
        duration = int(arguments["--duration"])
        duration_min = 2
        duration_max = 10
        if duration < duration_min or duration > duration_max:
            errors.append(
                "Duration has to be between %s and %s." % (
                    duration_min,
                    duration_max
                )
            )
    except ValueError:
        errors.append("Duration has to be an int.")

    # Handle errors
    if len(errors) > 0:
        print "Argument Error(s):"
        for error in errors:
            print " > %s" % error
        print "\nExiting..."
        sys.exit(1)

    if DEBUG:
        print "Running with parameters: interval: %s, duration: %s." % (interval, duration)

    images = grab_screen(interval, duration)

    tmp_fp, tmp_path = generate_gif(images, interval)

    if arguments["--clipboard"]:
        copy_to_clipboard(tmp_fp, tmp_path)
    else:
        save_gif(tmp_fp, tmp_path)

if __name__ == "__main__":
    main()
