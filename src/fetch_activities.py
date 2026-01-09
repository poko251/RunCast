import os
import pandas as pd
from datetime import datetime
from pathlib import Path

from strava_auth import get_strava_client
from scripts import format_time
def fetch_activities_with_stravalib(client, limit=100):
    """Download activities and saves raw"""
    
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
    "Takes important data from json and saves it to /processed as csv"
    newdf = pd.read_json(file_path)

    #COLUMNS: RAW TO CSV
    columns = ["moving_time", "distance" ,"total_elevation_gain", "id", "average_speed", "average_cadence", "has_heartrate", "average_heartrate", "max_heartrate", "type", "start_date", "map", "start_latlng", "end_latlng"] 

    #only runs
    newdf = newdf[newdf["type"] == "Run"]
    newdf = newdf[columns].copy()

    newdf = newdf.rename(columns={'id': 'real_id'})

    newdf["elapsed_time"] = newdf["moving_time"] 
    
    newdf["avg_cadence_real"] = newdf["average_cadence"] * 2
    newdf["elapsed_time_sec"] = newdf["elapsed_time"]
    newdf["average_speed_km/h"] = newdf["average_speed"] * 3.6
    newdf["elapsed_time_min"] = newdf["elapsed_time_sec"] / 60
    newdf["has_cadence"] = newdf["average_cadence"].notna().astype(int)
    newdf["has_heartrate"] = newdf["has_heartrate"].astype(int)
    newdf["distance_km"] = newdf["distance"] / 1000
    newdf["distance_m"] = newdf["distance"]
    newdf["pace_min/km"] = newdf["elapsed_time_min"] / newdf["distance_km"]
    newdf['start_date'] = pd.to_datetime(newdf['start_date'])
    newdf['polyline'] = newdf['map'].str.get('summary_polyline')
    newdf["pace_readable"] = newdf["pace_min/km"].apply(format_time)
    newdf["time_readable"] = newdf["elapsed_time_min"].apply(format_time)
    newdf["has_map"] = newdf["start_latlng"].notna().astype(int)
    newdf = newdf.sort_values(by='start_date', ascending=False).reset_index(drop=True)
    newdf['id'] = range(1, len(newdf) + 1)

        #cleaning outlayers
    newdf = newdf[newdf["distance_km"].between(1, 50)]
    newdf = newdf[newdf["elapsed_time_min"].between(5, 400)]
    newdf = newdf[newdf["pace_min/km"].between(3, 9)]
    newdf = newdf[newdf["total_elevation_gain"].between(0, 2000)]
    newdf = newdf[(newdf["average_heartrate"].isna()) | newdf["average_heartrate"].between(80, 200)]


    newdf = newdf.drop(["elapsed_time", "distance", "average_cadence"], axis=1)

    newdf = newdf[["real_id","pace_min/km", "elapsed_time_min", "distance_m", "distance_km", "has_heartrate", "average_heartrate", "max_heartrate", "has_cadence", "avg_cadence_real", "average_speed_km/h", "total_elevation_gain", "type", "start_date", "map", "polyline", "start_latlng", "end_latlng","pace_readable", "time_readable", "has_map","id"]]

    name = Path(file_path).stem

    output_dir = os.path.join("data", "personal", "processed")
    os.makedirs(output_dir, exist_ok=True)

    newdf.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)



if __name__ == "__main__":
    strava_client = get_strava_client()
    file_path = fetch_activities_with_stravalib(strava_client)
    take_important_data(file_path)