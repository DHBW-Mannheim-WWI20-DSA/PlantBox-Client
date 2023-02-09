import multiprocessing
import time
import os
from dotenv import load_dotenv
from functions.readSensor import read_data_from_sensors
from functions.pump import set_power

class StreamBuffer:
    def __init__(self, size: int = 10, sleep_time_sec: int = 10):
        self.buffer: list = list()  # Init empty Buffer
        self.size = size
        self.sleep_time_sec = sleep_time_sec
        self.min_moisture: float = 0.0
        self.max_moisture: float = 0.0
        self.storage_multiplier: int = 3
        self.secure_margin: float = 5.0
        self.queue = multiprocessing.Queue()
        self.exit = multiprocessing.Event()

    # Method to add Data to the Buffer
    def add_data(self, item):
        """
        :param item: Item to add to the Buffer
        :return: None
        """
        timestamp = time.time()
        if len(self.buffer) == self.size:
            self.buffer.pop(0)
        self.buffer.append([timestamp, round(item, 2)])
        self.queue.put(self.buffer)

    # Method to get the Buffer
    def get_data(self):
        """
        :return: last item in the buffer
        """
        return self.queue.get()

    # Method to read all Data from the Buffer
    def read_all_data(self):
        """
        :return: Buffer
        """
        return self.buffer

    def run_writing_process(self):
        while not self.exit.is_set():
            item = read_data_from_sensors()
            self.add_data(item)
            time.sleep(self.sleep_time_sec)
        self.queue.put(None)

    def run_processing_process(self):
        while True:
            item = self.get_data()
            if item is None:
                break
            self.run_control_pump(item)  # replace this with your function that processes data
            time.sleep(self.sleep_time_sec * self.storage_multiplier)

    # Method to control the Pump depending on the Data and the Environment Variables as Subprocess from a subprocess
    def run_control_pump(self, item: list[int, float]):
        """
        :param item: Item to process
        :return: None
        """
        # Loading of the Environment Variables
        if self.min_moisture is None:
            load_dotenv()
            self.min_moisture = float(int(os.environ.get('MIN_MOISTURE')))
        if self.max_moisture is None:
            load_dotenv()
            self.max_moisture = float(int(os.environ.get('MAX_MOISTURE')))
        # get last entry of the Buffer
        last_entry = item[-1]
        print(last_entry)
        # Activate Pump if the last entry is smaller than the minimum moisture
        if last_entry[1] < self.min_moisture + self.secure_margin:
            print(f'{time.ctime(last_entry[0])} - Pump Active - Moisture: {last_entry[1]} ')
            # Activate Pump
            set_power(True)
            # Decrease the sleep time to 1 second
            self.sleep_time_sec = 1
        # Deactivate Pump if the last entry is bigger than the maximum moisture
        elif last_entry[1] >= self.max_moisture - self.secure_margin:
            print(f'{time.ctime(last_entry[0])} - Pump Deactivate - Moisture: {last_entry[1]}')
            # Deactivate Pump
            set_power(False)
            # Increase the sleep time to 10 seconds
            self.sleep_time_sec = 10


def start_processes(stream_buffer):
    writing_process = multiprocessing.Process(target=stream_buffer.run_writing_process)
    processing_process = multiprocessing.Process(target=stream_buffer.run_processing_process)

    writing_process.start()
    processing_process.start()

    try:
        processing_process.join()
    except KeyboardInterrupt:
        stream_buffer.exit.set()
        writing_process.join()


if __name__ == '__main__':
    stream_buffer = StreamBuffer(10)
    start_processes(stream_buffer)
