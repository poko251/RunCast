import folium 
import pandas as pd
import ast
import polyline
import streamlit as st



def f_map(df, id):
    """creats map of a selected run"""
    selected_run = df[df['id'] == id].iloc[0]

    if selected_run["has_map"] == 0 :
        st.warning("This run has no GPS data.")
        return None
    else: 
        st.subheader("Map")
        start_coords = selected_run['start_latlng']
        start_l = ast.literal_eval(start_coords)
        start_l = tuple(start_l)

        end_coords = selected_run['end_latlng']
        end_l = ast.literal_eval(end_coords)
        end_l = tuple(end_l)

        encoded_polyline = selected_run['polyline']

        route_coordinates = polyline.decode(encoded_polyline)

        m = folium.Map(location=start_l)

        folium.Marker(
            location=start_l,
            tooltip="Start location",
            popup="Start location",
            icon=folium.Icon(color="green", icon="play"),
        ).add_to(m)

        folium.Marker(
            location=end_l,
            tooltip="End location",
            popup="End location",
            icon=folium.Icon(color="red", icon="stop"),
        ).add_to(m)


        folium.PolyLine(
            locations=route_coordinates,
            color="blue",       
            weight=5,           
            opacity=0.8,       
            tooltip="Run route"
        ).add_to(m)

        m.fit_bounds(route_coordinates)
        return m