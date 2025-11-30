from strava_auth import get_valid_acces_token
import requests
from datetime import datetime
import os
import json

def fetch_activities_from_strava(access_token, per_page=100, page=1):
    """Sends request to Strava Api and returns data"""


    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = f"https://www.strava.com/api/v3/athlete/activities?per_page={per_page}&page={page}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error {response.status_code}")
        return None
    
    activities = response.json()

    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join("data", "personal", "raw", f"{current_date}.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(activities, f, indent=4)

    print(f"Fetched{len(activities)} activities and saved to {file_path}")

if __name__ == "__main__":
    access_token = get_valid_acces_token()
    fetch_activities_from_strava(access_token)

def save_raw_json(activities, raw_dir):
    pass

def update_personal_csv(activities, csv_path):
    pass

def main(fetch_csv=True):
    pass