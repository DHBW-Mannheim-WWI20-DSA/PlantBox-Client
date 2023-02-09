import subprocess


def check_package_installed(package_name):
    try:
        output = subprocess.run(['dpkg-query', '-W', '-f=\'${Status}\n\'', package_name], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return True if 'install ok installed' in output.stdout.decode() else False
    except:
        return False


def install_package(package_name):
    # The command to run apt-get
    command = ['sudo', 'apt-get', 'install', '-y', package_name]

    # Run the command and capture the output
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors
    if output.returncode != 0:
        raise Exception(f'Error installing package {package_name}: {output.stderr.decode()}')


def set_power(state: bool):
    # The command to run usb-power-control
    command = ['sudo', 'uhubctl', '-l', '2', '-a']

    # Add the on/off option based on the state
    if state:
        command.append(1)
    else:
        command.append(0)

    # Run the command and capture the output
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors
    if output.returncode != 0:
        raise Exception(f'Error running usb-power-control: {output.stderr.decode()}')


# Define Function to toggle the USB Port which is connected to the Pump
def control_pump(enable: bool):
    pass


if __name__ == '__main__':
    control_pump(True)
    # control_pump(False)
