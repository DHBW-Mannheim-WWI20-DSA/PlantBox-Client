# Import of the necessary libraries
import os
import pathlib

from dotenv import load_dotenv


# Define function to read one environment variables from .env file
def readEnvFile(envFile: pathlib.Path, envVar: str):
    # Load environment variables from .env file
    load_dotenv(envFile)
    # Read environment variable and return it
    return os.getenv(envVar)


# Define function to write one environment variables to .env file
def writeEnvFile(envFile: pathlib.Path, envVar: str, envVal: str):
    # Load environment variables from .env file
    load_dotenv(envFile)
    # Save environment variables to .env file
    with open(envFile, 'w') as envFile:
        envFile.write(f'{envVar}={envVal}\n')
