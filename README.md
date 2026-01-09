# RunCast 

**RunCast** is an intelligent running dashboard that integrates Strava data with advanced ML analytics.

## Key Features

###  Automated Strava Sync
* **Direct API Integration:** Fetch your latest activities using the Strava API.
* **Smart Processing:** Automatic conversion of raw JSON data into clean, analyzed CSV datasets.
* **Outlier Detection:** Filtering to remove "noise" data (e.g., accidental recordings).

### Performance Analytics
* **Interactive Visualizations:** Ridge Plot, Pace Over Time, Zone Distribution.
* **Activity Heatmap:** Track consistency with a GitHub-style "contribution" calendar for your runs.
* **Interactive Mapping:** Fully interactive GPS maps for every activity using Folium and Polyline decoding.

###  AI Performance Predictor `BETA`
* **Riegel’s Baseline:** Compare predictions with the classic Riegel Formula based on your best historical performance.
* **XGBoost Regressor:** A Machine Learning model trained specifically on your running physiology.
* **kNN Augmentation:** Supplements your data with 200 "digital twin" activities from a global database of 40,000 runs to ensure accuracy even with few personal records.

## 🛠️ Technical Stack

### Frontend & UI
* **Streamlit** 
* **Folium & Streamlit-Folium** 

### Machine Learning & AI
* **XGBoost** 
* **Scikit-Learn** 
* **Joblib**

### 📊 Data Science & Analytics
* **Pandas** 
* **NumPy** 
* **Plotly & Ridgeplot** 

### ⚙️ Backend & Utilities
* **Stravalib** 
* **Python-Dotenv** 
* **Pathlib** 


## Project Structure

```text
runcast/
├── .env                    # Strava API Keys
├── .gitignore              
├── requirements.txt        # Python dependencies
├── dashboard/              # User Interface (Streamlit)
│   └── main.py             # Main entry point for the dashboard
├── src/                    # Core 
│   ├── model.py            # ML Logic BETA!!
│   ├── map.py              # GPS mapping logic
│   ├── plots.py            # Visualization logic 
│   ├── fetch_activities.py # Strava API pipeline
│   ├── riegel.py           # Mathematical formula
│   └── scripts.py          # Helper functions
├── models/                
│   └── xgb_running_model.joblib
├── data/                   # Data storage (Raw & Processed)
│   ├── personal/
│   └── public/
└── notebooks/              # Jupyter Notebooks
```

##  How to Run

### 1. Environment Setup
To sync with Strava, you need to provide your API credentials. Create a `.env` file in the **root folder** and paste your data:

```text
CLIENT_ID=your_strava_client_id
CLIENT_SECRET=your_strava_client_secret
```

### 2. Installation 

```text
pip install -r requirements.txt
```

### 3. Launch the Dashboard

Run the application from the root directory of the project using the following command:

```text
streamlit run dashboard/main.py
```