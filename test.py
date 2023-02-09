import pyudev

context = pyudev.Context()
for device in context.list_devices(subsystem='usb'):
    if 'ID_SERIAL' in device:
        print('{} ({})'.format(device['ID_SERIAL'], device.device_node))
    else:
        print('{}'.format(device.device_node))