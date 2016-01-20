#!/usr/bin/env python
"""
This Python script is designed to be executed from Monkey Runner tool
in the Android SDK.

This script send touch events to your device and takes screenshots
of your SWGOH squad, saving images at /tmp/swgoh-squad/ folder.
"""

import subprocess, os, sys, time, logging, signal
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

os.putenv('LANG', 'C')
logging.basicConfig(level=logging.INFO)

# Global reference to the device
logging.info("Waiting for device ...")
device = MonkeyRunner.waitForConnection()
logging.info("Connected to device %s" % (device.getProperty('build.model')))

# Folder used to save screenshots
FOLDER = "/tmp/swgoh-squad/"

def cleanup(signum, frame):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    device.shell('killall com.android.commands.monkey')
    sys.exit(1)

def snap(name, display=False):
    logging.debug('Taking screenshot of device ...')
    f = FOLDER + name + '.png'
    device.takeSnapshot().writeToFile(f, 'png')

    if display:
        cmd = ['display', '-resize', '1024x768', f]
        logging.debug('Running [%s]' % cmd)
        proc = subprocess.Popen(cmd)
        proc.wait()

def launch():
    package = 'com.ea.game.starwarscapital_row'
    activity = 'com.ea.games.capitalgames.CapitalGamesActivity'
    run = package + '/' + activity
    logging.info('Launching APK ...' + run)
    device.startActivity(component=run)

def touch(x, y):
    logging.debug("Sending touch event %d, %d", x, y)
    device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
    time.sleep(2)

def main():
    os.makedirs(FOLDER)
    logging.info("Initializing the program....")
    logging.info("*** Important! After you see a screenshot of your device, make sure the device")
    logging.info("    is awake and at the home of the game. Then click on the screenshot window on the PC")
    logging.info("    and press the 'q' key in your keyboard to start dumping the images.")

    launch()
    snap('device-homescreen', True)

    # Open characters screen
    touch(105, 300)
    time.sleep(3)
    
    # Open first char
    touch(213, 386)
    time.sleep(1)
    # Print all chars
    for i in range(71):
        logging.info("*** Snapping character #%d ...", i)
        logging.info("    Capturing basic info ...")
        snap('character-%02d-char' % i)

        touch(958, 1012)
        logging.info("    Capturing statistics")
        snap('character-%02d-stat' % i)
        touch(1540, 117)

        logging.info("    Done, moving to next one ...")
        touch(1217, 204)

    # TODO(ronoaldo): ocr all character screens to get the values we need
    logging.info("Finished! Now you can run the squadparse.sh script with Bash.")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup)
    main()
