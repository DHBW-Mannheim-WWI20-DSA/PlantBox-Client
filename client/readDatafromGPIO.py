import RPi.GPIO as GPIO


class ReadDataFromGPIO:
    """
    Class to read data from GPIO pin
    """

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def readData(self):
        return GPIO.input(self.pin)

    def readDataStream(self, stream_bool: bool = True):
        while stream_bool:
            yield GPIO.input(self.pin)

    def __del__(self):
        GPIO.cleanup()


if __name__ == '__main__':
    readDataFromGPIO = ReadDataFromGPIO(17)
    print(readDataFromGPIO.readData())
