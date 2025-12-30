from strava_auth import get_valid_acces_token
import requests
from datetime import datetime
import os
import json
import pandas as pd
from pathlib import Path

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
    return file_path


def take_important_data(file_path):
    "Takes important data from json and saves it to /processed as csv"
    df = pd.read_json(file_path)
    columns = ["elapsed_time", "distance" ,"total_elevation_gain", "id", "average_speed", "average_cadence", "has_heartrate", "average_heartrate", "max_heartrate"]

    newdf = df[columns].copy()

    newdf["avg_cadence_real"] = newdf["average_cadence"] * 2
    newdf["elapsed_time_sec"] = newdf["elapsed_time"]
    newdf["elapsed_time_min"] = newdf["elapsed_time_sec"] / 60
    newdf["has_cadence"] = newdf["average_cadence"].notna().astype(int)
    newdf["has_heartrate"] = newdf["has_heartrate"].astype(int)
    newdf["distance_km"] = newdf["distance"] / 1000
    newdf["distance_m"] = newdf["distance"]
    
    newdf = newdf.drop(["elapsed_time", "distance", "average_cadence"], axis=1)

    newdf = newdf[["id", "elapsed_time_min", "distance_m", "distance_km", "has_heartrate", "average_heartrate", "max_heartrate", "has_cadence", "avg_cadence_real", "average_speed", "total_elevation_gain"]]

    name = Path(file_path).stem

    output_dir = os.path.join("data", "personal", "processed")
    os.makedirs(output_dir, exist_ok=True)

    newdf.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)



if __name__ == "__main__":
    access_token = get_valid_acces_token()
    file_path = fetch_activities_from_strava(access_token)
    take_important_data(file_path)


