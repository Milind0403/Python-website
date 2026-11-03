
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌦️",
    layout="wide"
)

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #eef5fc;
}
.title {
    text-align: center;
    color: #1565c0;
    font-size: 35px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    '<div class="title">🌦️ Weather Forecast Dashboard</div>',
    unsafe_allow_html=True
)

st.write("### Check current weather and 7-day forecasts")
st.divider()

# AVAILABLE CITIES
cities = {
    "Nagpur": (21.1458, 79.0882),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639),
    "Jaipur": (26.9124, 75.7873),
    "Ahmedabad": (23.0225, 72.5714),
    "Nashik": (19.9975, 73.7898),
    "Indore": (22.7196, 75.8577),
    "Bhopal": (23.2599, 77.4126),
    "Surat": (21.1702, 72.8311),
    "Goa": (15.2993, 74.1240),
    "Lucknow": (26.8467, 80.9462),
    "Amritsar": (31.6340, 74.8723),
    "Patna": (25.5941, 85.1376),
    "Kochi": (9.9312, 76.2673),
    "Srinagar": (34.0837, 74.7973)
}

# WEATHER CONDITIONS
def get_weather(condition):
    weather = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Cloudy ☁️",
        45: "Foggy 🌫️",
        48: "Foggy 🌫️",
        51: "Light Drizzle 🌦️",
        53: "Drizzle 🌦️",
        55: "Heavy Drizzle 🌧️",
        61: "Light Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Light Snow ❄️",
        73: "Snowfall ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Showers 🌦️",
        81: "Rain Showers 🌧️",
        82: "Heavy Rain Showers 🌧️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm ⛈️",
        99: "Heavy Thunderstorm ⛈️"
    }
    return weather.get(condition, "Weather Unavailable")

# SELECT CITY
st.sidebar.title("🌍 Select City")

selected_city = st.sidebar.selectbox(
    "Choose Your City",
    list(cities.keys())
)

# REFRESH BUTTON
refresh = st.sidebar.button("🔄 Refresh Weather")

latitude, longitude = cities[selected_city]

# FETCH WEATHER DATA
@st.cache_data(ttl=600)
def get_weather_data(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weather_code"
        ],
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()
    return response.json()

if refresh:
    get_weather_data.clear()

try:
    data = get_weather_data(latitude, longitude)

    current = data["current"]
    daily = data["daily"]

    # CURRENT WEATHER
    st.subheader(f"📍 Current Weather - {selected_city}")

    st.markdown(
        f"## {get_weather(current['weather_code'])}"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡️ Temperature",
        f"{current['temperature_2m']} °C"
    )

    col2.metric(
        "💧 Humidity",
        f"{current['relative_humidity_2m']}%"
    )

    col3.metric(
        "💨 Wind Speed",
        f"{current['wind_speed_10m']} km/h"
    )

    col4.metric(
        "🌧️ Rainfall",
        f"{current['precipitation']} mm"
    )

    st.write(
        f"**Feels Like:** {current['apparent_temperature']} °C"
    )

    st.divider()

    # 7 DAY FORECAST
    st.subheader("📅 7-Day Weather Forecast")

    forecast_df = pd.DataFrame({
        "Date": daily["time"],
        "Maximum Temperature": daily["temperature_2m_max"],
        "Minimum Temperature": daily["temperature_2m_min"],
        "Rainfall": daily["precipitation_sum"],
        "Weather": [
            get_weather(code)
            for code in daily["weather_code"]
        ]
    })

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # TEMPERATURE CHART
    st.subheader("🌡️ Temperature Analysis")

    fig1 = px.line(
        forecast_df,
        x="Date",
        y=["Maximum Temperature", "Minimum Temperature"],
        markers=True,
        title="7-Day Temperature Forecast",
        template="plotly_white"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # RAINFALL CHART
    st.subheader("🌧️ Rainfall Analysis")

    fig2 = px.bar(
        forecast_df,
        x="Date",
        y="Rainfall",
        title="7-Day Rainfall Forecast",
        template="plotly_white"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # WEATHER SUMMARY
    st.subheader("📊 Weather Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Highest Temperature",
        f"{max(daily['temperature_2m_max'])} °C"
    )

    col2.metric(
        "Lowest Temperature",
        f"{min(daily['temperature_2m_min'])} °C"
    )

    col3.metric(
        "Expected Rainfall",
        f"{sum(daily['precipitation_sum']):.1f} mm"
    )

    st.success("Weather Forecast Loaded Successfully!")

except Exception as e:
    st.error("Unable to load weather data. Please check your internet connection and try again.")

# FOOTER
st.caption(
    "Weather Forecast Dashboard | Developed using Python and Streamlit"
)
