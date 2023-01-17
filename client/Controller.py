# Loading of Packages
import requests
from pid import PID
from client.readDatafromGPIO import ReadDataFromGPIO
from time import time
from client.connectServer import load_auth_data


# Define Function to Set up Configuration
def setup_config():
    # Load the Authentication Data
    connected_server = load_auth_data()
    # check if connected_server is registered
    if connected_server.client_id is None:
        # If not, register the Client
        connected_server.get_bearer_token()
        connected_server.register_client()
    # Return the Authentication Data
    return connected_server


# Define Function to send Data to the API
# data = dict(hydro_1 = SENSORWERT)
def send_data_to_api(connected_server, data):
    # Send a POST request to the API to send the Data
    response = requests.post(f'{connected_server.base_api_url}data/',
                             headers={f'Authorization ': '{} {}'.format(connected_server.token_type,
                                                                        connected_server.bearer_token)}, data=data)
    # If the response is successful, print the response
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code)


# Stream-buffer for Storing the Data
class StreamBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    def add(self, item):
        timestamp = time()
        if len(self.buffer) == self.size:
            self.buffer.pop(0)
        self.buffer.append([timestamp, item])

    def get_buffer(self):
        return self.buffer


# Define Function to read the Data from the Sensors
def read_data_from_sensors(GPIO_CONTROLLER: ReadDataFromGPIO, stream_buffer: StreamBuffer):
    # Read the Data from the Sensor
    data = GPIO_CONTROLLER.readData()
    # Add the Data to the Stream-buffer
    stream_buffer.add(data)
    # Return the Data
    return stream_buffer


# Define Function to calculate the PID-Values
def calculate_pid_values(stream_buffer: StreamBuffer, pid: PID):
    # Get the Data from the Stream-buffer
    data = stream_buffer.get_buffer()
    # Calculate the PID-Values
    pid_values = pid(data)
    # Return the PID-Values
    return pid_values
