import os
import pathlib
import pydantic
import uuid
import json
import requests
from dotenv import load_dotenv, set_key
from typing import Union


# Function to load the API URL from the .env file
def load_api_url():
    env_path = pathlib.Path.cwd()
    env_path = env_path.joinpath('.env')
    load_dotenv(dotenv_path=env_path)
    return os.getenv('API_URL') if os.getenv('API_URL') else None


# Load Authentication Data from file
def load_auth_data():
    env_path = pathlib.Path.cwd()
    env_path = env_path.joinpath('.env')
    load_dotenv(dotenv_path=env_path)
    connected_server = ConnectServer(
        username=os.getenv('ACCOUNT_NAME') if os.getenv('ACCOUNT_NAME') else None,
        password=os.getenv('ACCOUNT_PASSWORD') if os.getenv('ACCOUNT_PASSWORD') else None,
    )
    return connected_server


# Pydantic Model for Authentication Data
class ConnectServer(pydantic.BaseModel):
    username: str
    password: str
    client_id: Union[uuid.UUID, None] = None
    client_secret: Union[str, None] = None
    bearer_token: Union[str, None] = None
    token_type: Union[str, None] = None
    base_api_url: Union[str, None] = load_api_url()

    # Retrieve the Token from the API
    def get_bearer_token(self):
        if self.bearer_token is None:
            try:
                # Send a POST request to the API to retrieve the Token
                response = requests.post(f'{self.base_api_url}auth/login/',
                                         data=dict(username=self.username, password=self.password))
                # If the response is successful, set the Token
                if response.status_code == 200:
                    self.bearer_token = response.json()['access_token']
                    self.token_type = response.json()['token_type']
            except Exception as e:
                print(e)
        else:
            return dict(access_token=self.bearer_token, token_type=self.token_type)

    # Register the Client with the API
    def register_client(self):
        # If the Client ID is not set, register the Client
        if self.client_id is None:
            try:
                # Send a POST request to the API to register the Client
                response = requests.post(f'{self.base_api_url}auth/client/register',
                                         headers={f'Authorization': '{} {}'.format(self.token_type, self.bearer_token)})
                # If the response is successful, set the Client ID and Secret
                if response.status_code == 200:
                    self.client_id = uuid.UUID(response.json()['client_id'])
                    self.client_secret = response.json()['client_secret']
                    self.save_client_config()
            except Exception as e:
                print(e)
        else:
            return dict(client_id=self.client_id, client_secret=self.client_secret)

    # Save Client Config to .env file
    def save_client_config(self):
        env_path = pathlib.Path.cwd()
        env_path = env_path.joinpath('.env')
        load_dotenv(dotenv_path=env_path)
        set_key(dotenv_path=env_path, key_to_set='CLIENT_ID', value_to_set=str(self.client_id))
        set_key(dotenv_path=env_path, key_to_set='CLIENT_SECRET', value_to_set=self.client_secret)

    # Output the ConnectServer as a JSON String
    def __str__(self):
        return json.dumps(self.dict())


if __name__ == '__main__':
    connected_server = load_auth_data()
    connected_server.get_bearer_token()
    print(connected_server.bearer_token)
    connected_server.register_client()
    print(connected_server.client_id, connected_server.client_secret)
