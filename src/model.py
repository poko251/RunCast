import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import os 
from pathlib import Path

#BETA, FIX NEEDED

def read_data():
    """takes the latest CSV file and read it"""
    folder = Path("data/personal/processed")

    latest = max(folder.glob("*.csv"), key=lambda p: p.stem)
    df = pd.read_csv(str(latest)).copy()

    return df

my_df = read_data()
big_df = pd.read_csv("data/public/processed/df_big.csv")

def get_augmented_data(my_df, big_df, n_recent=25, neighbors_per_run=200):
    """Expands the user's dataset by finding similar activities in a global database using KNN."""
    knn_features = ['distance_km', 'total_elevation_gain', 'average_heartrate', 'has_heartrate']
    
    my_recent_runs = my_df.sort_values('start_date', ascending=False).head(n_recent).copy()
    
    def prep_for_knn(df):
        return df[knn_features].fillna(0).copy()
    
    big_df_features = prep_for_knn(big_df)
    my_features = prep_for_knn(my_recent_runs)


    scaler = StandardScaler()
    big_scaled = scaler.fit_transform(big_df_features)
    my_scaled = scaler.transform(my_features)

    knn = NearestNeighbors(n_neighbors=neighbors_per_run, metric='euclidean')
    knn.fit(big_scaled)
    
    distances, indices = knn.kneighbors(my_scaled)
    unique_indices = np.unique(indices.flatten())
    
    similar_runs = big_df.iloc[unique_indices].copy()
    similar_runs['is_mine'] = 0
    
    my_df_total = my_df.copy() 
    my_df_total['is_mine'] = 1
    
    final_df = pd.concat([my_df_total, similar_runs], ignore_index=True)
    
    return final_df
final_df = get_augmented_data(my_df, big_df)

def model(final_df):
    """Trains an XGBoost regressor using sample weights to prioritize personal data over global trends."""
    features = ['distance_km', 'total_elevation_gain', 'average_heartrate', 'has_heartrate']
    target = 'elapsed_time_min'


    X = final_df[features].fillna(0)
    y = final_df[target]

    weights = np.where(final_df['is_mine'] == 1, 100, 1)


    model_xgb = xgb.XGBRegressor(
        n_estimators=500,       
        learning_rate=0.05,      
        max_depth=4,            
        subsample=0.8,          
        random_state=42
    )

    model_xgb.fit(X, y, sample_weight=weights)


    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent 

    models_dir = project_root / "models"
    model_path = models_dir / "xgb_running_model.joblib"

    os.makedirs(models_dir, exist_ok=True)

    joblib.dump(model_xgb, model_path)


def make_prediction(dist, elev, hr_value, use_hr, model):
    """Predicts the total time and pace for a planned run based on distance, elevation, and heart rate."""
    features = ['distance_km', 'total_elevation_gain', 'average_heartrate', 'has_heartrate']
    
    if use_hr:
        hr_to_send = hr_value
        has_hr_flag = 1
    else:
        hr_to_send = 0
        has_hr_flag = 0
    
    input_data = pd.DataFrame([[dist, elev, hr_to_send, has_hr_flag]], columns=features)
    
    pred_minutes = model.predict(input_data)[0]
    pred_pace = pred_minutes / dist if dist > 0 else 0
    
    return pred_minutes, pred_pace