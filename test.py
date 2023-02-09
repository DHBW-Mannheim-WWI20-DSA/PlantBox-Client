import multiprocessing
import time

from functions.readSensor import read_data_from_sensors


class StreamBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.sleep_time_sec = 10
        self.queue = multiprocessing.Queue()
        self.exit = multiprocessing.Event()

    # Method to add Data to the Buffer
    def add_data(self, item):
        """
        :param item: Item to add to the Buffer
        :return: None
        """
        self.queue.put([time.time(), round(item, 2)])

    # Method to get the Buffer
    def get_data(self):
        """
        :return: Buffer
        """
        return self.queue.get()

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
            print(item)  # replace this with your function that processes data
            time.sleep(self.sleep_time_sec * 5)


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
