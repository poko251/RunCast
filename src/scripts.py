import pandas as pd

def format_time(pace_decimal):
    if pd.isna(pace_decimal) or pace_decimal == 0:
        return "-"
    minutes = int(pace_decimal)
    seconds = int(round((pace_decimal - minutes) * 60))
    
    if seconds == 60:
        minutes += 1
        seconds = 0
        
    return f"{minutes}:{seconds:02d}"

def clean_nan(val, decimals=None):
    if pd.isna(val):
        return "-"
    if decimals is not None:
        return round(val, decimals)
    return val