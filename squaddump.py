import subprocess, os, sys, time, logging, signal
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

os.putenv('LANG', 'C')
logging.basicConfig(level=logging.DEBUG)

# Global reference to the device
logging.info("Waiting for device ...")
device = MonkeyRunner.waitForConnection()
logging.info("Connected to device %s" % (device.getProperty('build.model')))

def cleanup(signum, frame):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    device.shell('killall com.android.commands.monkey')
    sys.exit(1)

def snap(name, display=False):
    logging.debug('Taking screenshot of device ...')
    f = '/tmp/squaddump-' + name + '.png'
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
    logging.info("Sending touch event %d, %d", x, y)
    device.touch(x, y, MonkeyDevice.DOWN_AND_UP)
    time.sleep(2)

def main():
    launch()
    snap('homescreen', True)
    
    # Open characters screen
    touch(105, 300)
    snap('characters')
    
    # Open first char
    touch(213, 386)
    time.sleep(1)
    # Print all chars
    for i in range(71):
        logging.info(">>> Snapping character %d ...", i)
        snap('character-%02d-char' % i)

        touch(958, 1012)
        snap('character-%02d-stat' % i)
        touch(1540, 117)

        logging.info("<<< Moving to next one ...")
        touch(1217, 204)

    # TODO(ronoaldo): ocr all character screens to get the values we need
    logging.info("Finished!")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup)
    main()
