# Import of Libraries
from time import sleep
from smbus2 import SMBus


# Define Function to read the Data from the Sensors
def read_data_from_sensors(i2c_number: int = 1, i2c_address: int = 0x48, i2c_channel: int = 2):
    """
    Read Data from the Sensor
    :param i2c_number: I2C-Busnummer (0 für Revision 1, 1 für Revision 2)
    :param i2c_address: I2C-Adresse des AD-Wandlers (0x48 ist die Standardadresse)
    :param i2c_channel: Register des AD-Wandlers, das die Daten des Sensors enthält
    :return: soil_moisture: Soil Moisture in Percent
    """
    # Read Data from Sensor
    data = SMBus(i2c_number).read_byte_data(i2c_address, i2c_channel)
    # Transform Data to Percent
    soil_moisture = (195 - data) / (195 - 75) * 100
    # Return the Data
    return soil_moisture


if __name__ == '__main__':
    while True:
        print(read_data_from_sensors())
        sleep(1)
