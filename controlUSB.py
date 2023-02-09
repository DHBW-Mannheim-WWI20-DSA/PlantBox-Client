import subprocess


# Method to change Power-state of the USB-Port
def set_power(state: bool):
    # The command to run usb-power-control
    command = ['sudo', 'uhubctl', '-l', '2', '-a']

    # Add the on/off option based on the state
    if state:
        command.append("1")
        print("Power on")
    else:
        command.append("0")
        print("Power off")

    # Run the command and capture the output
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    print(set_power(True))
