########################################################################################################################
# arcom.py
#
# Contains all the low level utility functions used to talk to and interact with the PythonSlave Arduino sketch.
########################################################################################################################


__author__ = 'Christopher Broussard'

DEBUG_LEVEL = 1 # 1?

# Define some constants that correspond to values used on the Arduino itself.
INPUT = 0
OUTPUT = 1
HIGH = 1
LOW = 0


# These are the opcodes we use when talking to the Arduino.  They define the
# command we want to execute.  There is a 1 to 1 correspondence between these
# opcodes and the ones defined on the Arduino.
class OpCodes:
    SetPin = 0
    GetPin = 1
    SetPinMode = 2


def set_pinmode(arduino_com, pin, pinmode):
    """
    Sets the pinmode for the designated pin.

    @param arduino_com: Serial port object connected to the Arduino.
    @type arduino_com: serial.Serial
    @param pin: The pin to set.
    @type pin: int
    @param pinmode: The pin mode.
    @type pinmode: int
    """

    # Send the pinmode.
    arduino_com.flushInput()
    arduino_com.write("{0} {1} {2}\n".format(OpCodes.SetPinMode, pin, pinmode).encode('ascii'))


    # Wait for the echo string.
    wait_for_response(arduino_com)


def set_pin(arduino_com, pin, pin_value):
    """
    Sets the pin value for the designated pin.

    @param arduino_com: Serial port object connected to the Arduino.
    @type arduino_com: serial.Serial
    @param pin: The pin to set.
    @type pin: int
    @param pin_value: The pin value.
    @type pin_value: int
    """

    # Send the pin value.
    arduino_com.write("{0} {1} {2}\n".format(OpCodes.SetPin, pin, pin_value).encode('utf-8'))

    # Wait for the echo string.
    wait_for_response(arduino_com)


def get_pin(arduino_com, pin):
    """
    Gets the pin value for the designated pin.

    @param arduino_com: Serial port object connected to the Arduino.
    @type arduino_com: serial.Serial
    @param pin: The pin to set.
    @type pin: int
    @return: The current value of the pin.
    @rtype: int
    """

    # Request the pin value.
    arduino_com.write("{0} {1}\n".format(OpCodes.GetPin, pin).encode('utf-8'))

    # Wait for the echo string, which will contain the pin value.
    return int(wait_for_response(arduino_com))


def wait_for_response(arduino_com):
    """
    Wait for a response from the Arduino and returns it as a string
    with the newline character stripped off.

    @param arduino_com: Serial port object connected to the Arduino.
    @type arduino_com: serial.Serial
    @return: Response from the Arduino
    @rtype: str
    """

    while arduino_com.inWaiting() == 0:
        pass

    echo = arduino_com.readline().strip().decode("utf-8")

    if DEBUG_LEVEL > 0: # ??? DEBUG_LEVEL is never changed 0 > 0 is false
        print(('Echo String: ' + echo))

    return echo
