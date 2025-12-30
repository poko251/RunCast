import pandas as pd
import numpy as np
import os

def dataset1():
    "cleaning dataset1"
    df = pd.read_csv("data/public/raw-data-kaggle.csv", sep=";")


    df["distance_km"] = df["distance (m)"] /1000 
    df["elapsed_time_min"] = df["elapsed time (s)"] /60
    df.rename(columns={"average heart rate (bpm)": "avg_hr"}, inplace=True)
    df["pace_min_per_km"] = df["elapsed_time_min"] / df["distance_km"]

    #cleaning outlayers
    df = df[df["distance_km"].between(1, 50)]
    df = df[df["elapsed_time_min"].between(5, 400)]
    df = df[df["pace_min_per_km"].between(3, 9)]
    df = df[df["elevation gain (m)"].between(0, 2000)]
    df = df[(df["avg_hr"].isna()) | df["avg_hr"].between(80, 200)]

    df.reset_index(drop=True, inplace=True)

    df["has_hr"] = df["avg_hr"].notna().astype(int)
    df["source"] = 0
    df["speed_kmh"] = df["distance_km"] / (df["elapsed_time_min"] / 60 )

    df.rename(columns={"elapsed time (s)":"elapsed_time_sec", "distance (m)":"distance_m", "has_hr":"has_heartrate","avg_hr":"average_heartrate", "speed_kmh": "average_speed", "elevation gain (m)": "total_elevation_gain"},inplace=True)

    df = df.drop(columns=["timestamp", "gender", "athlete", "elapsed_time_sec"], axis=1)
    return df


def dataset2():
    "cleaning dataset2"
    df = pd.read_csv("data/public/strava_full_data.csv", sep=",")
    df = df[df["type"] == "Run"]

    df.rename(columns={"average_heartrate": "avg_hr"}, inplace=True)


    df["distance_km"] = df["distance"] / 1000
    df['elapsed_time'] = pd.to_timedelta(df['elapsed_time'])
    df['elapsed_time_min'] = df['elapsed_time'].dt.total_seconds() / 60
    df["pace_min_per_km"] = df["elapsed_time_min"] / df["distance_km"]
    df["source"] = 1
    df["speed_kmh"] = (df["distance_km"] ) / (df["elapsed_time_min"] / 60)
    
    #cleaning outlayers
    df = df[df["distance_km"].between(1, 50)]
    df = df[df["elapsed_time_min"].between(5, 400)]
    df = df[df["pace_min_per_km"].between(3, 9)]
    df = df[df["total_elevation_gain"].between(0, 2000)]
    df = df[(df["avg_hr"].isna()) | df["avg_hr"].between(80, 200)]
    df.reset_index(drop=True, inplace=True)

    df = df.drop(columns="average_speed")
    df.rename(columns={"elapsed time (s)":"elapsed_time_sec", "distance (m)":"distance_m", "has_hr":"has_heartrate","avg_hr":"average_heartrate", "speed_kmh": "average_speed", "elevation gain (m)": "total_elevation_gain"}, inplace=True)

    df = df.drop(columns=["Unnamed: 0", "kudos_count", "start_date_local", "moving_time", "max_speed", "max_heartrate", "elapsed_time", "elev_high", "type"])
    df = df.rename(columns={"distance":"distance_m"})

    return df


def concat():
    
    df1 = dataset1()
    df2 = dataset2()

    df_big = pd.concat([df1, df2], ignore_index=True)

    output_dir = os.path.join("data", "public","processed")
    os.makedirs(output_dir, exist_ok=True)

    df_big.to_csv(os.path.join(output_dir, "df_big.csv"), index=False)

    

concat()