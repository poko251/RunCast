import streamlit as st

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




