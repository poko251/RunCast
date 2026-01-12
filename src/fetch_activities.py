import os
import pandas as pd
from datetime import datetime
from pathlib import Path

from strava_auth import get_strava_client
from scripts import format_time
def fetch_activities_with_stravalib(client, limit=100):
    """Download activities and saves raw in data/personal/raw"""
    
    activities = list(client.get_activities(limit=limit))
    
    raw_data = []
    for a in activities:
        raw_data.append(a.model_dump(mode='json'))

    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join("data", "personal", "raw", f"{current_date}.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    import json
    with open(file_path, "w") as f:
        json.dump(raw_data, f, indent=4) 

    return file_path

def take_important_data(file_path):
    """Extracts, cleans and processes Strava run data and saves it as CSV in data/personal/processed"""
    df = pd.read_json(file_path)

    #COLUMNS: RAW TO CSV
    
    BASE_COLUMNS = [
        "moving_time", "distance", "total_elevation_gain", "id",
        "average_speed", "average_cadence", "has_heartrate",
        "average_heartrate", "max_heartrate", "type",
        "start_date", "map", "start_latlng", "end_latlng"
    ]


    #only runs
    df = df[df["type"] == "Run"]
    df = df[BASE_COLUMNS].copy()

    df = df.rename(columns={'id': 'real_id'})

    df["elapsed_time"] = df["moving_time"] 
    
    df["avg_cadence_real"] = df["average_cadence"] * 2
    df["elapsed_time_sec"] = df["elapsed_time"]
    df["average_speed_km/h"] = df["average_speed"] * 3.6
    df["elapsed_time_min"] = df["elapsed_time_sec"] / 60
    df["has_cadence"] = df["average_cadence"].notna().astype(int)
    df["has_heartrate"] = df["has_heartrate"].astype(int)
    df["distance_km"] = df["distance"] / 1000
    df["distance_m"] = df["distance"]
    df["pace_min/km"] = df["elapsed_time_min"] / df["distance_km"]
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['polyline'] = df['map'].str.get('summary_polyline')
    df["pace_readable"] = df["pace_min/km"].apply(format_time)
    df["time_readable"] = df["elapsed_time_min"].apply(format_time)
    df["has_map"] = df["start_latlng"].notna().astype(int)
    df = df.sort_values(by='start_date', ascending=False).reset_index(drop=True)
    df['id'] = range(1, len(df) + 1)

        #cleaning outlayers
    df = df[df["distance_km"].between(1, 50)]
    df = df[df["elapsed_time_min"].between(5, 400)]
    df = df[df["pace_min/km"].between(3, 9)]
    df = df[df["total_elevation_gain"].between(0, 2000)]
    df = df[(df["average_heartrate"].isna()) | df["average_heartrate"].between(80, 200)]


    df = df.drop(["elapsed_time", "distance", "average_cadence"], axis=1)

    FINAL_COLUMNS = ["real_id","pace_min/km", "elapsed_time_min", "distance_m", "distance_km", "has_heartrate", "average_heartrate", "max_heartrate", "has_cadence", "avg_cadence_real", "average_speed_km/h", "total_elevation_gain", "type", "start_date", "map", "polyline", "start_latlng", "end_latlng","pace_readable", "time_readable", "has_map","id"]

    df = df[FINAL_COLUMNS]

    name = Path(file_path).stem

    output_dir = os.path.join("data", "personal", "processed")
    os.makedirs(output_dir, exist_ok=True)

    df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)



if __name__ == "__main__":
    strava_client = get_strava_client()
    file_path = fetch_activities_with_stravalib(strava_client)
    take_important_data(file_path)