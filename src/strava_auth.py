import os
import time
from dotenv import load_dotenv, set_key
from stravalib.client import Client

def load_env_data():
    load_dotenv()
    return {
        "client_id": os.getenv("STRAVA_CLIENT_ID"),
        "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
        "access_token": os.getenv("STRAVA_ACCESS_TOKEN"),
        "expires_at": os.getenv("STRAVA_EXPIRES_AT"),
    }

def update_env_file(access_token, refresh_token, expires_at):
    env_path = ".env"
    set_key(env_path, "STRAVA_ACCESS_TOKEN", access_token)
    set_key(env_path, "STRAVA_REFRESH_TOKEN", refresh_token)
    set_key(env_path, "STRAVA_EXPIRES_AT", str(expires_at))

def get_strava_client():
    env = load_env_data()
    client = Client()

    client.refresh_token = env["refresh_token"]

    #checks if token is expireed
    expires_at = int(env["expires_at"]) if env["expires_at"] else 0
    now = int(time.time())

    if now > expires_at:
        token_response = client.refresh_access_token(
            client_id=env["client_id"],
            client_secret=env["client_secret"],
            refresh_token=env["refresh_token"]
        )

        update_env_file(
            token_response['access_token'],
            token_response['refresh_token'],
            token_response['expires_at']
        )
        
        client.access_token = token_response['access_token']
    else:
        print("Token jest nadal ważny.")
        client.access_token = env["access_token"]

    return client