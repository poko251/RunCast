import streamlit as st
from pathlib import Path
import pandas as pd
import sys
import plotly.graph_objects as go

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))
from src.plots import (
    draw_ridge_plot,
    pace_zones_distribution,
    draw_pace_over_time,
    distance_distribution,
    draw_github_calendar
)



def read_data():
    folder = Path("data/personal/processed")

    #takes the latest file
    latest = max(folder.glob("*.csv"), key=lambda p: p.stem)
    df = pd.read_csv(str(latest)).copy()

    st.dataframe(df)

    return df

def summary(df):
    total_distance = df["distance_km"].sum()
    total_runs = df["id"].count()
    total_time = df["elapsed_time_min"].sum()
    # avg_pace = df["pace_min/km"].avg()

    #best 5km
    filtered_df_5km = df[df['distance_km'] < 5.15]
    fastest_row_5km = filtered_df_5km.sort_values(by='elapsed_time_min').iloc[0]

    pace_5km = fastest_row_5km['pace_min/km']
    time_5km = fastest_row_5km['elapsed_time_min']


    #best 10km

    filtered_df_10km = df[df['distance_km'] < 10.15]
    fastest_row_10km = filtered_df_10km.sort_values(by='elapsed_time_min').iloc[0]

    pace_10km = fastest_row_10km['pace_min/km']
    time_10km = fastest_row_10km['elapsed_time_min']


    stats = [
        {"label": "Pace_5km", "pace": f"{pace_5km}km", "Time_5km": f"{time_5km}min"} ,
        {"label": "Pace_10km", "value": f"{pace_5km}km"} ,
        {"label": "Pace_5km", "value": f"{pace_5km}km"} 
    ]
    

    col_total_time, col_total_min = st.columns(2)

    # with col_total_time:
    #     tile = st.container(height=80)
    #     tile.write = ("xdd")


def riegel(t1, d1, d2):
    if d1 == 0:
        raise ValueError("d1 must be > 0")
    
    t2 = t1 * (d2 / d1) ** 1.06
    st.write(f"Your time will be {t2}")
    return 

def riegel_choose_activity(df):
    options = df["id"].tolist()

    selected_id = st.selectbox(
        "Wybierz aktywność",
        options
    )
    selected_row = df[df["id"] == selected_id].iloc[0]

    return float(selected_row["distance_km"]), float(selected_row["elapsed_time_min"])














st.title("RUNCAST")
st.write("Input your distance")




if __name__ == "__main__":
    df = read_data()
    distance, time = riegel_choose_activity(df)

    d2 = st.text_input("Distance:")

    if d2:
        d2 = float(d2)
        t2 = riegel(time, distance, d2)

    pace_zones_distribution(df)
    draw_ridge_plot(df)
    distance_distribution(df)
    draw_pace_over_time(df)
    draw_github_calendar(df)
    summary(df)