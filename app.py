<<<<<<< HEAD

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Example dataset ---
np.random.seed(42)
years = list(range(2015, 2025))
countries = ['Australia', 'Brazil', 'Canada']
minerals = ['Copper', 'Iron', 'Lithium']

data = []
for country in countries:
    for mineral in minerals:
        for year in years:
            data.append({
                'Country': country,
                'Mineral': mineral,
                'Year': year,
                'Price': np.random.randint(50, 200),
                'Reserves': np.random.randint(1000, 5000),
                'Demand': np.random.randint(200, 1000)
            })

df = pd.DataFrame(data)

# --- Streamlit UI ---
st.title("Mineral Dashboard")

# Sidebar for selection
selected_country = st.sidebar.selectbox("Select Country", df['Country'].unique())
selected_mineral = st.sidebar.selectbox("Select Mineral", df['Mineral'].unique())

filtered_df = df[(df['Country'] == selected_country) & (df['Mineral'] == selected_mineral)]

# --- Line chart: Price over Years ---
st.subheader(f"{selected_mineral} Price over Years in {selected_country}")
fig_price = px.line(filtered_df, x='Year', y='Price', markers=True)
st.plotly_chart(fig_price)

# --- Multi-axis comparison: Price vs Reserves vs Demand ---
st.subheader(f"Multi-axis Comparison (Price vs Reserves vs Demand)")

fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Price'], name='Price', yaxis='y1', mode='lines+markers'))
fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Reserves'], name='Reserves', yaxis='y2', mode='lines+markers'))
fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Demand'], name='Demand', yaxis='y3', mode='lines+markers'))

fig.update_layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Price', side='left'),
    yaxis2=dict(title='Reserves', overlaying='y', side='right'),
    yaxis3=dict(title='Demand', overlaying='y', side='right', position=0.95),
    legend=dict(y=1.1, orientation='h')
)

st.plotly_chart(fig)
>>>>>>> 9b3cde4bea1b3bead4d0fbcda09ce6caae233e50
