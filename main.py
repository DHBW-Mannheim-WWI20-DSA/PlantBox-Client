# Import of the necessary libraries
import os
import time
import asyncio
from dotenv import load_dotenv
from readSensor import read_data_from_sensors
from controlUSB import set_power
from websocket import create_connection

# Define global variables
global_buffer = list()


# Define async function to read data from the sensors
async def run_data_to_buffer(buffer: list, sleep_time_sec: int = 1):
    while True:
        item_time = time.time()
        item_value = read_data_from_sensors()
        if len(buffer) == 10:
            buffer.pop(0)
        buffer.append([item_time, item_value])
        await asyncio.sleep(sleep_time_sec)


# Define async function to control the pump
async def run_pump_control(buffer: list, sleep_time_sec: int = 1, min_moisture: float = 40.0,
                           max_moisture: float = 80.0):
    while True:
        if len(buffer) >= 5:
            # Calculate the average of the last 5 values
            average = sum([item[1] for item in buffer[-5:]]) / 5
            print("Average Moisture: " + str(average))
            # Check if the average is below the minimum value
            if average < min_moisture:
                set_power(True)
            elif average >= max_moisture:
                set_power(False)
        await asyncio.sleep(sleep_time_sec)


# Define async function to send data to the server
async def run_data_to_server(buffer: list, sleep_time_sec: int = 1):
    load_dotenv()
    while True:
        # Check if the buffer is not empty and have at least 5 values
        if len(buffer) >= 5:
            # get the last 5 values
            last_five = buffer[-5:]
            # prepare the data for the server transmission
            data = {
                "auth_token": os.getenv('AUTH_TOKEN'),
                "time": [item[0] for item in last_five],
                "value": [item[1] for item in last_five]
            }
            print(data)
            # establish the connection to the server
            ws = create_connection(os.getenv('SERVER_URL'))
            # send the data to the server
            ws.send(str(data))
            # Wait for the server response
            result = ws.recv()
            if result == "200":
                print("Data sent to server")
                buffer[:] = buffer[-len(buffer) + 5:]
            else:
                print("Error while sending data to server")
            # close the connection to the server
            ws.close()
        await asyncio.sleep(sleep_time_sec)


# Define main function
async def main():
    # Starte alle asynchronen Funktionen
    task1 = asyncio.create_task(run_data_to_buffer())
    task2 = asyncio.create_task(run_pump_control())
    task3 = asyncio.create_task(run_data_to_server())

    await asyncio.gather(task1, task2, task3)


# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
