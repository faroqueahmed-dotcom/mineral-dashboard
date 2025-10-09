import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------
# Generate Example Dataset
# -------------------
np.random.seed(42)
countries = ["Chile", "Australia", "South Africa"]
minerals = ["Copper", "Iron Ore", "Gold"]
dates = pd.date_range("2020-01-01", periods=24, freq="M")

data = []
for country in countries:
    for mineral in minerals:
        base_price = np.random.randint(50, 200) * 10
        base_reserve = np.random.randint(200, 500)
        base_demand = np.random.randint(100, 400)

        # simulate time trends
        trend_price = np.linspace(0, np.random.randint(-500, 500), len(dates))
        trend_reserve = np.linspace(0, np.random.randint(-50, 50), len(dates))
        trend_demand = np.linspace(0, np.random.randint(-100, 100), len(dates))

        # noise
        noise_price = np.random.normal(0, base_price * 0.05, len(dates))
        noise_reserve = np.random.normal(0, base_reserve * 0.05, len(dates))
        noise_demand = np.random.normal(0, base_demand * 0.05, len(dates))

        prices = base_price + trend_price + noise_price
        reserves = base_reserve + trend_reserve + noise_reserve
        demand = base_demand + trend_demand + noise_demand

        for d, p, r, dem in zip(dates, prices, reserves, demand):
            data.append([country, mineral, d, round(p, 2), round(r, 2), round(dem, 2)])

df = pd.DataFrame(data, columns=["Country", "Mineral", "Date", "Price", "Reserves", "Demand"])

# -------------------
# Streamlit Dashboard
# -------------------
st.set_page_config(page_title="Mineral Analytics Dashboard", layout="wide")
st.title("🌍 Bilateral Mineral Trade Dashboard")
st.markdown("<i style='color: #888;'>Developed by Dr. Kazi Sohag & Faroque Ahmed</i>", unsafe_allow_html=True)


# Sidebar filters
st.sidebar.header("Filters")
countries_selected = st.sidebar.multiselect("Select Countries", df["Country"].unique(), default=["Chile"])
minerals_selected = st.sidebar.multiselect("Select Minerals", df["Mineral"].unique(), default=["Copper"])
chart_type = st.sidebar.radio("Select Chart Type", ["Line", "Bar", "Scatter", "Multi-Axis Comparison"])

# Filter data
filtered = df[(df["Country"].isin(countries_selected)) & (df["Mineral"].isin(minerals_selected))]

# -------------------
# Visualizations
# -------------------
st.subheader("📈 Price Trends / Reserves / Demand")

if chart_type in ["Line", "Bar"]:
    for var in ["Price", "Reserves", "Demand"]:
        st.markdown(f"### {var} Trends")
        if chart_type == "Line":
            fig = px.line(filtered, x="Date", y=var, color="Country", line_dash="Mineral",
                          title=f"{var} over Time")
        else:
            fig = px.bar(filtered, x="Date", y=var, color="Country", barmode="group",
                         facet_row="Mineral", title=f"{var} over Time")
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter":
    st.markdown("### Scatter Comparisons")
    scatter_var_x = st.selectbox("Select X Variable", ["Price", "Reserves", "Demand"])
    scatter_var_y = st.selectbox("Select Y Variable", ["Price", "Reserves", "Demand"], index=1)
    fig = px.scatter(filtered, x=scatter_var_x, y=scatter_var_y, color="Country",
                     size="Demand", symbol="Mineral", hover_data=["Date"],
                     title=f"{scatter_var_y} vs {scatter_var_x}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Multi-Axis Comparison":
    st.markdown("### Multi-Axis Comparison (Price vs Reserves vs Demand)")
    for country in countries_selected:
        for mineral in minerals_selected:
            subdf = filtered[(filtered["Country"] == country) & (filtered["Mineral"] == mineral)]
            if not subdf.empty:
                fig = go.Figure()

                fig.add_trace(go.Scatter(x=subdf["Date"], y=subdf["Price"],
                                         mode="lines+markers", name="Price", yaxis="y1"))
                fig.add_trace(go.Scatter(x=subdf["Date"], y=subdf["Reserves"],
                                         mode="lines+markers", name="Reserves", yaxis="y2"))
                fig.add_trace(go.Scatter(x=subdf["Date"], y=subdf["Demand"],
                                         mode="lines+markers", name="Demand", yaxis="y3"))

                fig.update_layout(
                    title=f"{mineral} in {country}",
                    xaxis=dict(domain=[0.1, 0.85]),
                    yaxis=dict(
                        title=dict(text="Price", font=dict(color="blue")),
                        tickfont=dict(color="blue")
                    ),
                    yaxis2=dict(
                        title=dict(text="Reserves", font=dict(color="red")),
                        tickfont=dict(color="red"),
                        anchor="free", overlaying="y", side="left", position=0.05
                    ),
                    yaxis3=dict(
                        title=dict(text="Demand", font=dict(color="green")),
                        tickfont=dict(color="green"),
                        anchor="x", overlaying="y", side="right"
                    ),
                    legend=dict(x=1.05, y=1)
                )
                st.plotly_chart(fig, use_container_width=True)

# -------------------
# Raw Data
# -------------------
with st.expander("🔎 Show Raw Data"):
    st.dataframe(filtered)
