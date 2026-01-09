import streamlit as st
from pathlib import Path
import pandas as pd
import sys
from streamlit_folium import st_folium
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from src.plots import (
    draw_ridge_plot,
    pace_zones_distribution,
    draw_pace_over_time,
    distance_distribution,
    draw_github_calendar
)

from src.riegel import riegel, riegel_choose_activity
from src.scripts import format_time, clean_nan
from src.map import f_map

st.set_page_config(
    page_title="Runcast Dashboard",
    layout="wide", 
    initial_sidebar_state="expanded"
)



def read_data():
    folder = Path("data/personal/processed")

    #takes the latest file
    latest = max(folder.glob("*.csv"), key=lambda p: p.stem)
    df = pd.read_csv(str(latest)).copy()

    return df


def summary(df):
    total_distance = df["distance_km"].sum()
    total_runs = df["id"].count()
    total_time = df["elapsed_time_min"].sum()
    total_time = format_time(total_time)

    avg_pace = df["pace_min/km"].mean()
    avg_pace = format_time(avg_pace)

    #best 5km
    filtered_df_5km = df[(df['distance_km'] >= 4.8) & (df['distance_km'] < 5.5)]
    if not filtered_df_5km.empty:
        fastest_row_5km = filtered_df_5km.sort_values(by='elapsed_time_min').iloc[0]
    else:
        pace_5km, time_5km = "-", "-"
    print(fastest_row_5km)
    pace_5km = fastest_row_5km['pace_readable']
    time_5km = fastest_row_5km['time_readable']

    #best 10km

    filtered_df_10km = df[(df['distance_km'] >= 9.8) & (df['distance_km'] < 11)]
    if not filtered_df_10km.empty:
        fastest_row_10km = filtered_df_10km.sort_values(by='elapsed_time_min').iloc[0]
    else:
        pace_10km, time_10km = "-", "-"

    pace_10km = fastest_row_10km["pace_readable"]
    time_10km = fastest_row_10km["time_readable"]



    with st.container(border=False):
        col1, col2, col3, col4 = st.columns(4, border=True)
        col5, col6 = st.columns(2, border=True)

        with col1:
            st.metric("Total distance", f"{round((total_distance), 2)}km")

        with col2:
            st.metric("Total runs", total_runs)
        
        with col3:
            st.metric("Total time", f"{total_time}min")

        with col4:
            st.metric("Average pace", f"{avg_pace}min/km")


        with col5:
            st.subheader("Best 5km")
            st.metric("Pace", f"{pace_5km}min/km")
            st.metric("Time", f"{time_5km}min")

        
        with col6:
            st.subheader("Best 10km")
            st.metric("Pace", f"{pace_10km}min/km")
            st.metric("Time", f"{time_10km}min")


def plots_dashboard(df):
    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Calendar")
        
        with col2:
            df["start_date"] = pd.to_datetime(df["start_date"])
            options = df["start_date"].dt.year.unique()
            year = st.selectbox(
            "Choose year",
            options)


        draw_github_calendar(df, year)


    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            pace_zones_distribution(df)
        
        with col2:
            distance_distribution(df)

    with st.container(border=True):
        draw_pace_over_time(df)

    with st.container(border=True):
            draw_ridge_plot(df)

def show_data(df):
    columns = ["id","date", "distance_km", "time_readable", "average_heartrate", "has_map"]
    st.dataframe(df[columns], hide_index=True)

def choose_run(df):
    options = df["id"]
    id = st.selectbox(
        "Choose run (id)",
        options 
    )
    return id

def run_map(df, id):

    m = f_map(df, id)

    if m is not None:
        st_folium(m,width="stretch" ,height=500)
    
def run_stats(df, id):
    selected_run = df[df['id'] == id].iloc[0]

    #date, distance, time, heart_rate, max_hr, cadence, pace, elevation_gain 

    raw_delta = ((df["pace_min/km"].mean() - selected_run["pace_min/km"]) / df["pace_min/km"].mean()) * 100


    date = clean_nan(selected_run["date"])
    distance = clean_nan(selected_run["distance_km"], 2)
    time = clean_nan(selected_run["time_readable"])
    hr = clean_nan(selected_run["average_heartrate"])
    max_hr = clean_nan(selected_run["max_heartrate"])
    cadence = clean_nan(selected_run["avg_cadence_real"])
    pace = clean_nan(selected_run["pace_readable"])
    speed = clean_nan(selected_run["average_speed_km/h"], 2)
    elev = clean_nan(selected_run["total_elevation_gain"])

    delta_pace = clean_nan(raw_delta, 1)

    st.subheader(date)

    col1, col2 ,col3, col4 = st.columns(4, border=True)
    col5, col6, col7, col8 = st.columns(4, border=True)
    with col1:
        st.metric("Distance", f"{distance}km")

    with col2:
        st.metric("Time", f"{time}min")
    
    with col3:
        st.metric("Pace", f"{pace}min/km", f"{delta_pace:.1f}% vs Average" )

    with col4:
        st.metric("Speed", f"{speed}km/h")

    with col5:
        st.metric("Average Heart Rate", f"{hr}bpm")

    with col6:
        st.metric("Max Heart Reate", f"{max_hr}min")
    
    with col7:
        st.metric("Cadence", f"{cadence}spm")

    with col8:
        st.metric("Total elevation gain", f"{elev}m")


        





if __name__ == "__main__":
    df = read_data()
    st.title("RUNCAST")
    tab1, tab2, tab3 = st.tabs(["Summary", "Run", "Prediction"])
    with tab1:
        summary(df)
        plots_dashboard(df)

    with tab2:
        show_data(df)
        id = choose_run(df)
        run_stats(df, id)
        run_map(df, id)

    with tab3:
        d1, t1 = riegel_choose_activity(df)
        d2 = 5
        t2 = riegel(t1, d1, d2)

        # distance, time = riegel_choose_activity(df)

    # d2 = st.text_input("Distance:")

    # if d2:
    #     d2 = float(d2)
    #     t2 = riegel(time, distance, d2)
