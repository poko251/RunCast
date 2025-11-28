import os
import requests
import time
from dotenv import load_dotenv

#loads values from .env file and return it as dict
def load_env():
    load_dotenv()

    env = {
        "client_id": os.getenv("STRAVA_CLIENT_ID"),
        "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
        "access_token": os.getenv("STRAVA_ACCESS_TOKEN"),
        "expires_at": os.getenv("STRAVA_EXPIRES_AT"),
    }

    return env

#refresh access_token using refresh_token and updates venv
def refresh_access_token():
    env = load_env()

    client_id = env["client_id"]
    client_secret = env["client_secret"]
    refresh_token = env["refresh_token"]


    url = "https://www.strava.com/oauth/token"

    payload = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
}
    
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print("Error refreshing token:", response.text)
        raise Exception("Failed to refresh token")
    
    data = response.json()

    new_access_token = data["access_token"]
    new_refresh_token = data["refresh_token"]
    expires_at = data["expires_at"]

    with open(".env", "r") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        if line.startswith("STRAVA_ACCESS_TOKEN"):
            new_lines.append(f"STRAVA_ACCESS_TOKEN={new_access_token}\n")
        elif line.startswith("STRAVA_REFRESH_TOKEN"):
            new_lines.append(f"STRAVA_REFRESH_TOKEN={new_refresh_token}\n")
        elif line.startswith("STRAVA_EXPIRES_AT"):
            new_lines.append(f"STRAVA_EXPIRES_AT={expires_at}\n")
        else:
            new_lines.append(line)

    with open(".env", "w") as f:
        f.writelines(new_lines)

    return new_access_token

#checks if access_token is valid, if not refresh it
def get_valid_acces_token():
    env = load_env()

    expires_at = int(env["expires_at"])
    now = int(time.time())

    if expires_at > now:
        return env["access_token"]
    
    else:
        new_token = refresh_access_token()
        return new_token