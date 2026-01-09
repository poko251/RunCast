import matplotlib.pyplot as plt
import plotly.express as px 
import numpy as np
from ridgeplot import ridgeplot
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def pace_zones_distribution(df):

    bins = [0, 4.0, 4.5, 5.0, 6.0, float('inf')]

    labels = [
    'Very Fast (< 4:00)', 
    'Fast (4:00 - 4:30)', 
    'Moderate (4:30 - 5:00)', 
    'Easy (5:00 - 6:00)', 
    'Recovery (> 6:00)'
    ]  
    

    df['zone'] = pd.cut(df['pace_min/km'], bins=bins, labels=labels, right=False)
    zone_counts = df['zone'].value_counts().reindex(labels).fillna(0)

    df_pie = zone_counts.reset_index()
    df_pie.columns = ['Zone', 'Number']

    fig = px.pie(
        df_pie, 
        values='Number', 
        names='Zone', 
        title='Pace Zone Distribution',
        color_discrete_sequence=px.colors.qualitative.Safe, 
        hole=0.4 
    )

    
    st.plotly_chart(fig, width='stretch')

def distance_distribution(df):
    bins = [0, 5.0, 10.0, 15.0, 21.1, float('inf')]
    
    labels = [
        'Short  (< 5 km)', 
        'Standard (5 - 10 km)', 
        'Medium (10 - 15 km)', 
        'Long (15 - 21.1 km)', 
        'Halfmarathon+ (> 21.1 km)'
    ]

    df['dist_category'] = pd.cut(df['distance_km'], bins=bins, labels=labels, right=False)
    
    dist_counts = df['dist_category'].value_counts().reindex(labels).fillna(0)


    df_dist_pie = dist_counts.reset_index()
    df_dist_pie.columns = ['Category', 'Number']


    fig = px.pie(
        df_dist_pie, 
        values='Number', 
        names='Category', 
        title='Distance distribution',
        color_discrete_sequence=px.colors.qualitative.Pastel, 
        hole=0.4 
    )

    st.plotly_chart(fig, width='stretch')

def draw_ridge_plot(df):

    df['start_date'] = pd.to_datetime(df['start_date'])
    df['day_name'] = df['start_date'].dt.day_name()
    df['hour'] = df['start_date'].dt.hour
    

    desired_order = ["Sunday", "Saturday", "Friday", "Thursday", "Wednesday", "Tuesday", "Monday"]
    
    samples = []
    labels = []

    for day in desired_order:
        day_hours = df[df['day_name'] == day]['hour'].values
        if len(day_hours) >= 2: 
            samples.append(day_hours)
            labels.append(day)

    if not samples:
        st.info("Add more runs")
        return

    fig = ridgeplot(
        samples=samples,
        labels=labels,
        bandwidth=1.8,
        kde_points=np.linspace(0, 24, 500),
        colorscale="viridis",
        colormode="row-index",
        opacity=0.7,
        spacing=0.5,
    )

    fig.update_layout(
        title="Distribution of runs during the day",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    
        margin=dict(l=150, r=40, t=40, b=60),
        
        height=600,
        font=dict(size=14), 
        
        xaxis=dict(
            title="Hour of Day",
            range=[0, 24],
            tickvals=[0, 6, 12, 18, 24],
            ticktext=["12 AM", "6 AM", "12 PM", "6 PM", "12 AM"],
            gridcolor="rgba(128, 128, 128, 0.2)", 
            zeroline=False,
            showgrid=True
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,

            showticklabels=True,
            automargin=True
        ),
        showlegend=False
    )


    fig.update_traces(line=dict(color='black', width=1.5))

    st.plotly_chart(fig, width='stretch')

def draw_github_calendar(df, year):
    df['date'] = pd.to_datetime(df['start_date']).dt.date
    daily_km = df.groupby('date')['distance_km'].sum()

    all_days = pd.date_range(f"{year}-01-01", f"{year}-12-31")
    z_values = [daily_km.get(d.date(), 0) for d in all_days]
    
    weeks = [d.isocalendar()[1] for d in all_days]
    weekdays = [d.weekday() for d in all_days]

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=weeks,
        y=weekdays,
        colorscale=[[0, '#151B23'], [0.1, '#9be9a8'], [0.5, '#40c463'], [1, '#216e39']],
        showscale=False,
        xgap=3, ygap=3,
        hoverinfo="text",
        text=[f"Date: {d.strftime('%d %b')}<br>Distance: {z:.2f} km" for d, z in zip(all_days, z_values)]
    ))

    fig.update_layout(
        height=200,
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 2, 4, 6],
            ticktext=['Mon', 'Wed', 'Fri', 'Sun'],
            autorange="reversed",
            fixedrange=True
        ),
        xaxis=dict(showgrid=False, fixedrange=True, title="Week of Year"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=10, l=10, r=10)
    )

    st.plotly_chart(fig, width='stretch')


def draw_pace_over_time(df):
    df['start_date'] = pd.to_datetime(df['start_date'])
    df = df.sort_values('start_date')

    fig = px.line(
        df, 
        x='start_date', 
        y='pace_min/km',
        title='Pace over time',
        markers=True,              
        hover_data={
            'pace_min/km': False,       
            'pace_readable': True,   
            'time_readable': True,    
            'distance_km': ':.2f',    
            'start_date': '|%B %d, %Y'  
        },
        labels={
            'pace_readable': 'Pace',
            'time_readable': 'Duration',
            'distance_km': 'Distance'
        }
    )

    fig.update_yaxes(autorange="reversed")


    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
        height=500
    )


    fig.update_traces(line_color='#1f77b4', marker=dict(size=8, color='#ff7f0e'))

    st.plotly_chart(fig, width='stretch')
