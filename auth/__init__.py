# Import Libraries
import os
import requests
from dotenv import load_dotenv

# FastAPI
import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import Functions
from functions.envFile import readEnvFile, writeEnvFile

# Load Environment Variables
load_dotenv(override=True)


# Define Function for first Setup
def init_setup():
    """
    This function is used to set up the environment for the first time.
    """
    # Define Basic FastAPI App
    app = FastAPI()

    # Define Templates
    templates = Jinja2Templates(directory="templates")

    # Define Static Files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Define Routes
    @app.get("/", response_class=HTMLResponse)
    def read_root(request: Request, response: Response):
        return templates.TemplateResponse("auth_login.html", {"request": request})

    @app.post("/")
    async def setup_get(request: Request):
        load_dotenv()
        form_data = await request.form()
        # Load Server URL
        print(os.getenv("SERVER_URL"))
        server_url = os.getenv("SERVER_URL") + "/token-user"
        # Check if Form fields are not empty
        print(form_data)
        print(server_url)
        if form_data["username"] and form_data["password"]:
            # Request to server URL
            response = requests.post(server_url, data={"username": form_data["username"], "password": form_data["password"]})
            print(response)
    uvicorn.run(app, host="127.0.0.1", port=8080)


# Define Function to check if the Environment is set up
def check_setup() -> bool:
    """
    This function is used to check if the environment is set up.
    """
    return os.getenv("REGISTERED") if os.getenv("REGISTERED") else False


# Define Main Function
def main():
    """
    This function is used to run the main program.
    """
    if check_setup():
        init_setup()
    else:
        pass


# Run Main Function
if __name__ == '__main__':
    main()
