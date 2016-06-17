#### Notes
#

# Start program
# delay for several minutes
# Open valve X for 1 minute
# *** Record pokes
# Close valve X
# Wait ITI ~3minutes
# Do that N times
# Do odor trial
# added distractor valve Mike Dryden 11/17/2015

__author__ = 'Christopher Broussard'
__editors__ = ['Mike Dryden', 'Tom Mast', 'Joseph Johnson']

import sys
import imp
import serial
import time
import arcom
from configparser import ConfigParser

config = ConfigParser()
MASTGUI = ("C:/Users/Tom Mast/Desktop/WinPython-64bit-3.4.3.5/python-3.4.3.amd64/Scripts/MASTconfig.ini")
config.read(MASTGUI)



class Solenoid:
    """
    Simple class that defines a solenoid.  Currently only only two variables: pin and name.
    The pin is the physical Arduino pin that the solenoid ultimately connects to.  The name can be any
    arbitrary string, but is intended to hold the name of the odor associated with the solenoid.
    """

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin


def run_trials(test_pattern):
    """
    Runs through a set of solenoids specified in the test pattern.

    :param test_pattern:
    """
    print(test_pattern)
   
    # Iterate over all the solenoids in the test pattern.
    for i_valve in test_pattern:
        print(i_valve)
        print(type(i_valve))
        # Pull out the trial solenoid.
        solenoid = solenoids[i_valve - 1]

        arcom.set_pin(arduino_com, LED_PIN, arcom.HIGH)
        # Open the valve.
        arcom.set_pin(arduino_com, solenoid.pin, arcom.HIGH)
        

        # Turn DISTRACTOR valve on.
        #arcom.set_pin(arduino_com, DISTRACTOR_PIN, arcom.HIGH)

        # Turn the LED on.
        #arcom.set_pin(arduino_com, LED_PIN, arcom.HIGH)

        # Log that we've opened the solenoid.
        solenoid_open_time = get_timestamp()
        fid.write('{0}\tODOR_ON\t{1}\n'.format(solenoid_open_time, solenoid.name))
        fid.flush()

        # Check the nose pokes while the valve is open.
        t0 = time.time()
        last_nosepoke_state = 0
        while time.time() - t0 < TRIAL_DURATION:
            # Get the current nose poke value.
            nosepoke_value = arcom.get_pin(arduino_com, NOSEPOKE_PIN)

            # Get the time we checked the nose port.
            nosepoke_time = get_timestamp()

            # If the last nosepoke state was 'unpoked' and the current one
            # is 'poked', count that as a single nose poke.
            if last_nosepoke_state == 0 and nosepoke_value == 1:
                # Write the poke to the output file.
                fid.write('{0}\tPOKE_ENTER\n'.format(nosepoke_time))
                fid.flush()
            elif last_nosepoke_state == 1 and nosepoke_value == 0:
                fid.write('{0}\tPOKE_EXIT\n'.format(nosepoke_time))
                fid.flush()

            # Store the nose poke value so we can compare it to later
            # poke values.
            last_nosepoke_state = nosepoke_value

        # Close the valve.
        arcom.set_pin(arduino_com, solenoids[i_valve-1].pin, arcom.LOW)
        # Turn the DISTRACTOR valve off.
        #arcom.set_pin(arduino_com, DISTRACTOR_PIN, arcom.LOW)

        # Turn the LED off.
        arcom.set_pin(arduino_com, LED_PIN, arcom.LOW)

        # Log that we've closed the solenoid.
        solenoid_close_time = get_timestamp()
        fid.write('{0}\tODOR_OFF {1}\n'.format(solenoid_close_time, solenoid.name))
        fid.flush()

        # Turn on ITI valve and Wait the ITI time then turn off ITI valve
        arcom.set_pin(arduino_com, ITI_PIN, arcom.HIGH)
        print("ITI valve on")
        time.sleep(ITI)
        arcom.set_pin(arduino_com, ITI_PIN, arcom.LOW)
        print("ITI valve off")

def get_timestamp():
    """
    Gets the current time and converts it into a log format compatible with the commercial
    olfactometer output, which looks like "Hour:Minute:Seconds".

    :rtype : str
    :return: The time string "Hour:Minute:Seconds".  Example: 12:34:9.23423
    """

    # Get the current time in seconds since the epoch.
    t = time.time()

    # Convert the seconds into a time structure.
    time_struct = time.localtime(t)

    # The time structure doesn't maintain the fractional seconds data, so get that
    # ourselves.
    seconds_fraction = str(t).split('.')[1]

    # Format everything into a string and return it.
    return time.strftime("%H:%M:%S", time_struct) + "." + seconds_fraction



def convertToList(l):
    
    l = list(map(int,l.replace("[","").replace("]","").split(",")))
    return l

def read(section, key):
    try:

        # :rtype : int
        return config.getint(section, key)

    # ask-for-forgiveness-not-permission
    except ValueError:
        # :rtype : str
        l = config.get(section, key)
        a = convertToList(l)
        return a



# This is the port and baud rate for talking to the Arduino.
# On Windows setups, the serial port will look something like 'COM3'.
SERIAL_PORT = 'COM4'
BAUD_RATE = 57600

# Create a list of all of our solenoids.  Each solenoid is given a name, which should indicate the odor it releases,
# and a pin value which corresponds to which Arduino it is hooked up to.
solenoids = [Solenoid("Blank odor", 22),
             Solenoid("Mineral Oil", 24),
             Solenoid("Test Odor", 26),
             Solenoid("General Stink", 28),
             Solenoid("Rat Poison", 30),
             Solenoid("Love Musk", 32),
             Solenoid("Roses", 34),
             Solenoid("Bald Eagle Tears", 36)]

# Nose poke pin.
NOSEPOKE_PIN = 2

# Pin for the DISTRACTOR valve.
#DISTRACTOR_PIN = 53

# Pin for the ITI valve
ITI_PIN = 22

# Pin for the LED.
LED_PIN = 38

# Habituation solenoid pattern.  The indices into the solenoid array.
"""
HABITUATION_PATTERN = config.getint("Sequence", "HABITUATION_PATTERN") #int

See .read() method
"""

HABITUATION_PATTERN = read("Sequence", "HABITUATION_PATTERN")




# Test solenoid pattern.
TEST_PATTERN = read("Sequence", "TEST_PATTERN")



# Start delay in seconds.
START_DELAY = 0.1*60

# Inter trial interval in seconds.
ITI = read("Timing", "ITI")

# Trial duration (valve open time) in seconds.
TRIAL_DURATION = 0.1*60

# Output file to write to
OUTPUT_FILE = 'C:/Users/Tom Mast/Desktop/5_26_16 Dryden Test Test.txt'

# Open the output file.
fid = open(OUTPUT_FILE, 'w')

# Open the connection to the Arduino.
arduino_com = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Give the Arduino a couple of seconds to process
# the connection.  For some computers, there seems
# to be a lag from the time we connect via serial
# to when the Arduino actually responds to serial
# input.
time.sleep(2)

# Clear anything that's on the serial port connection.  We don't care
# about any communication at this point.
arduino_com.flush()

# Set the solenoid pins to outputs.
for s in solenoids:
    arcom.set_pinmode(arduino_com, s.pin, arcom.OUTPUT)

# Set the nosepoke pin to be an input.
arcom.set_pinmode(arduino_com, NOSEPOKE_PIN, arcom.INPUT)

# Do the program start delay.
time.sleep = (START_DELAY)

# First we'll run the habituation trials.
print('- Running habituation trials')
run_trials(HABITUATION_PATTERN)

# Now run the test trials.
print('- Running test trials')
run_trials(TEST_PATTERN)

# Close the Arduino connection and file.
arduino_com.close()
fid.close()
