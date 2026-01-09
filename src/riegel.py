import streamlit as st

def predict_riegel(df, target_distance_km):
    if df.empty:
        return None, None, 0

    available_runs = min(len(df), 10)
    recent_runs = df.sort_values('start_date', ascending=False).head(available_runs)

    best_recent_run = recent_runs.sort_values('pace_min/km').iloc[0]
    
    T1 = best_recent_run['elapsed_time_min']
    D1 = best_recent_run['distance_km']
    D2 = target_distance_km
    
    predicted_time = T1 * (D2 / D1)**1.06
    
    predicted_pace = predicted_time / D2
    
    return predicted_time, predicted_pace
