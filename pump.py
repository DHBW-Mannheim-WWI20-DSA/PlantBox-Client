import os

# Path to the USB power control file
power_file = '/sys/bus/usb/devices/1-1/power/control'


def set_power(state):
    with open(power_file, 'w') as f:
        f.write('on' if state else 'off')


if __name__ == '__main__':
    # Turn on power to the USB port
    set_power(True)

    # Turn off power to the USB port
    set_power(False)
