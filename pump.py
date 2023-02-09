import subprocess


def install_package(package_name):
    # The command to run apt-get
    command = ['sudo', 'apt-get', 'install', '-y', package_name]

    # Run the command and capture the output
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors
    if output.returncode != 0:
        raise Exception(f'Error installing package {package_name}: {output.stderr.decode()}')


def set_power(state):
    # The command to run usb-power-control
    command = ['sudo', 'usb-power-control', '--bus', '1', '--device', '1']

    # Add the on/off option based on the state
    if state:
        command.append('--on')
    else:
        command.append('--off')

    # Run the command and capture the output
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors
    if output.returncode != 0:
        raise Exception(f'Error running usb-power-control: {output.stderr.decode()}')


# Define Function to toggle the USB Port which is connected to the Pump
def control_pump(enable: bool):
    # Check if the usb-power-control package is installed
    try:
        output = subprocess.run(['dpkg-query', '-W', '-f=\'${Status}\n\'', 'usb-power-control'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if 'install ok installed' not in output.stdout.decode():
            install_package('usb-power-control')
    except:
        install_package('usb-power-control')

    # Turn on/off the USB port
    set_power(enable)


if __name__ == '__main__':
    control_pump(True)
    # control_pump(False)
