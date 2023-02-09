# Import of Libraries
import multiprocessing
import time

# Import of Classes
from classes.StreamBuffer import StreamBuffer

# Import of Functions
from functions.envFile import readEnvFile, writeEnvFile
from functions.readSensor import read_data_from_sensors


# Define Sub-Procedure for reading the Data from the Sensors
def worker_gather_Data(streambuffer: StreamBuffer, sleep_time_sec: int, stop_event: multiprocessing.Event):
    while not stop_event.is_set():
        # Read Data from the Sensors
        soil_moisture = read_data_from_sensors()
        # Add the Data to the Buffer
        streambuffer.add(soil_moisture)
        # Wait for sleep_time_sec seconds
        time.sleep(sleep_time_sec)


# Define Sub-Procedure for sending the Data to the Server
def worker_send_Data(streambuffer: StreamBuffer, sleep_time_sec: int, stop_event: multiprocessing.Event):
    while not stop_event.is_set():
        # Get the Buffer
        buffer = streambuffer.get_buffer()
        # Send the Data to the Server
        print(buffer)
        # Delete the Data from the Buffer
        for entry in buffer:
            try:
                for i in range(len(streambuffer.buffer)):
                    if streambuffer.buffer[i] == entry:
                        streambuffer.buffer.pop(i)
            except IndexError:
                pass
        # Wait for sleep_time_sec seconds
        time.sleep(sleep_time_sec * 5)


def main():
    # Define the Buffer
    streambuffer = StreamBuffer(10)
    # Define the sleep_time_sec
    sleep_time_sec = 10
    # Define the stop_event
    stop_event = multiprocessing.Event()

    # Start multiple worker processes
    processes = [
        multiprocessing.Process(target=worker_gather_Data, args=(streambuffer, sleep_time_sec, stop_event)),
        multiprocessing.Process(target=worker_send_Data, args=(streambuffer, sleep_time_sec, stop_event))
    ]
    for process in processes:
        process.start()

    try:
        # Do some other work here
        while True:
            print("Main process is running")
            time.sleep(1)

    except KeyboardInterrupt:
        # Set the stop event to terminate all worker processes
        stop_event.set()

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
