import folium 
import pandas as pd
import ast
import polyline



df = pd.read_csv("data/personal/processed/2026-01-08.csv")

map_df = df[["start_latlng", "end_latlng", "polyline"]].dropna()

start_location = map_df["start_latlng"].iloc[2]
start_l = ast.literal_eval(start_location)
start_l = tuple(start_l)

end_location = map_df["end_latlng"].iloc[2]
end_l = ast.literal_eval(end_location)
end_l = tuple(end_l)

encoded_polyline= map_df["polyline"].iloc[2]

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
    tooltip="Trasa biegu"
).add_to(m)

m.save("index.html")