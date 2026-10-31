
import streamlit as st
import pandas as pd
import plotly.express as px
import random

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Weather Data Analyzer",
    page_icon="🌦️",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f0f6fc;
}
.title {
    text-align: center;
    color: #1565c0;
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------

st.markdown(
    '<div class="title">🌦️ Weather Data Analyzer System</div>',
    unsafe_allow_html=True
)

st.write(
    "### Weather Monitoring, Visualization and Statistical Analysis"
)

st.divider()

# -------------------------------
# GENERATE SAMPLE DATA
# -------------------------------

@st.cache_data
def generate_weather_data():

    random.seed(42)

    dates = pd.date_range(
        start="2026-01-01",
        periods=30,
        freq="D"
    )

    data = {
        "Date": dates,
        "Temperature": [
            random.randint(18, 40) for _ in dates
        ],
        "Humidity": [
            random.randint(30, 95) for _ in dates
        ],
        "Wind Speed": [
            round(random.uniform(2, 25), 2)
            for _ in dates
        ],
        "Rainfall": [
            round(random.uniform(0, 30), 2)
            for _ in dates
        ]
    }

    return pd.DataFrame(data)


df = generate_weather_data()

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("⚙️ Dashboard Settings")

st.sidebar.write("Select Weather Parameters")

selected_city = st.sidebar.selectbox(
    "Select City",
    ["Pune", "Mumbai", "Delhi", "Chennai", "Bangalore"]
)

st.sidebar.write("Upload Your Own Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        uploaded_df = pd.read_csv(uploaded_file)

        required_columns = [
            "Date",
            "Temperature",
            "Humidity",
            "Wind Speed",
            "Rainfall"
        ]

        if all(col in uploaded_df.columns for col in required_columns):
            df = uploaded_df.copy()
            df["Date"] = pd.to_datetime(df["Date"])
            st.sidebar.success("Dataset uploaded successfully!")
        else:
            st.sidebar.error(
                "CSV must contain: Date, Temperature, Humidity, Wind Speed, Rainfall"
            )

    except Exception as e:
        st.sidebar.error(f"Error reading CSV: {e}")

# -------------------------------
# WEATHER DATA
# -------------------------------

st.subheader(f"📍 Weather Dashboard - {selected_city}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌡️ Average Temperature",
    f"{df['Temperature'].mean():.1f} °C"
)

col2.metric(
    "💧 Average Humidity",
    f"{df['Humidity'].mean():.1f}%"
)

col3.metric(
    "💨 Average Wind Speed",
    f"{df['Wind Speed'].mean():.1f} km/h"
)

col4.metric(
    "🌧️ Total Rainfall",
    f"{df['Rainfall'].sum():.1f} mm"
)

st.divider()

# -------------------------------
# DATA TABLE
# -------------------------------

st.subheader("📋 Weather Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# -------------------------------
# TEMPERATURE ANALYSIS
# -------------------------------

st.subheader("🌡️ Temperature Analysis")

fig1 = px.line(
    df,
    x="Date",
    y="Temperature",
    markers=True,
    title="Daily Temperature Analysis",
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# HUMIDITY ANALYSIS
# -------------------------------

st.subheader("💧 Humidity Analysis")

fig2 = px.bar(
    df,
    x="Date",
    y="Humidity",
    title="Daily Humidity Analysis",
    template="plotly_white"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# WIND SPEED ANALYSIS
# -------------------------------

st.subheader("💨 Wind Speed Analysis")

fig3 = px.area(
    df,
    x="Date",
    y="Wind Speed",
    title="Wind Speed Analysis",
    template="plotly_white"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# RAINFALL ANALYSIS
# -------------------------------

st.subheader("🌧️ Rainfall Analysis")

fig4 = px.bar(
    df,
    x="Date",
    y="Rainfall",
    title="Daily Rainfall Analysis",
    template="plotly_white"
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# STATISTICAL ANALYSIS
# -------------------------------

st.subheader("📊 Statistical Weather Analysis")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Maximum Temperature",
    f"{df['Temperature'].max()} °C"
)

col2.metric(
    "Minimum Temperature",
    f"{df['Temperature'].min()} °C"
)

col3.metric(
    "Average Temperature",
    f"{df['Temperature'].mean():.2f} °C"
)

st.write("### Additional Statistics")

st.write("Average Humidity:", round(df["Humidity"].mean(), 2), "%")
st.write("Maximum Wind Speed:", round(df["Wind Speed"].max(), 2), "km/h")
st.write("Total Rainfall:", round(df["Rainfall"].sum(), 2), "mm")

# -------------------------------
# CORRELATION ANALYSIS
# -------------------------------

st.subheader("📈 Weather Correlation Analysis")

corr = df[
    ["Temperature", "Humidity", "Wind Speed", "Rainfall"]
].corr()

fig5 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Weather Parameter Correlation",
    aspect="auto"
)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# DOWNLOAD REPORT
# -------------------------------

st.divider()

st.subheader("📥 Download Weather Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Weather Data CSV",
    data=csv,
    file_name="weather_report.csv",
    mime="text/csv"
)

st.success("Weather Data Analysis Completed Successfully!")

st.caption(
    "Weather Data Analyzer System | Developed using Python and Streamlit"
)
