# Import of Libraries
from time import time


# Define Storage Buffer
class StreamBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    # Method to add Data to the Buffer
    def add(self, item):
        """
        :param item: Item to add to the Buffer
        :return: None
        """
        timestamp = time()
        if len(self.buffer) == self.size:
            self.buffer.pop(0)
        self.buffer.append([timestamp, round(item, 2)])

    # Method to get the Buffer
    def get_buffer(self):
        """
        :return: Buffer
        """
        return self.buffer

    # Method to delete one Item from the Buffer
    def delete_item(self, index):
        """
        :param index: Index of the Item to delete
        :return: None
        """
        self.buffer.pop(index)

    # Method to delete all Items from the Buffer
    def delete_all_items(self):
        """
        :return: None
        """
        self.buffer = []

    # Method to get the current Size of the Buffer
    def get_current_size(self):
        """
        :return: Current Size of the Buffer
        """
        return len(self.buffer)

    # Method to delete multiple Items from the Buffer
    def delete_multiple_items(self, start_index, end_index):
        """
        :param start_index: Index of the first Item to delete
        :param end_index: Index of the last Item to delete
        """
        self.buffer = self.buffer[:start_index] + self.buffer[end_index:]