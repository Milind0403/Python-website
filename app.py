
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Weather Data Analyzer",
    page_icon="🌦️",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>
.main {
    background-color: #f4f8fc;
}
.title {
    text-align: center;
    color: #1565c0;
    font-size: 38px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
}
.metric-card {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

st.markdown(
    '<div class="title">🌦️ Weather Data Analyzer System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Real-Time Weather Monitoring and Data Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------
# API CONFIGURATION
# --------------------------------

st.sidebar.header("⚙️ Settings")

st.sidebar.write("Enter your OpenWeatherMap API key.")

api_key = st.sidebar.text_input(
    "API Key",
    type="password"
)

city = st.sidebar.text_input(
    "Enter City Name",
    value="Pune"
)

analyze = st.sidebar.button(
    "Analyze Weather",
    type="primary",
    use_container_width=True
)

# --------------------------------
# API URLS
# --------------------------------

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# --------------------------------
# FETCH WEATHER DATA
# --------------------------------

def get_weather(city, api_key):

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        CURRENT_URL,
        params=params,
        timeout=15
    )

    if response.status_code != 200:
        raise ValueError(
            response.json().get(
                "message",
                "Unable to fetch weather data."
            )
        )

    return response.json()


# --------------------------------
# FETCH FORECAST DATA
# --------------------------------

def get_forecast(city, api_key):

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=15
    )

    if response.status_code != 200:
        raise ValueError(
            response.json().get(
                "message",
                "Unable to fetch forecast data."
            )
        )

    return response.json()


# --------------------------------
# WEATHER ANALYSIS
# --------------------------------

if analyze:

    if not api_key.strip():
        st.error("Please enter your OpenWeatherMap API key.")

    elif not city.strip():
        st.error("Please enter a city name.")

    else:

        try:

            with st.spinner("Fetching weather data..."):

                weather = get_weather(city, api_key)
                forecast = get_forecast(city, api_key)

            st.success(
                f"Weather data loaded successfully for {weather['name']}!"
            )

            # Current Weather Information

            st.subheader("📍 Current Weather Information")

            col1, col2, col3, col4 = st.columns(4)

            temperature = weather["main"]["temp"]
            humidity = weather["main"]["humidity"]
            wind_speed = weather["wind"]["speed"]
            pressure = weather["main"]["pressure"]

            col1.metric(
                "🌡️ Temperature",
                f"{temperature} °C"
            )

            col2.metric(
                "💧 Humidity",
                f"{humidity}%"
            )

            col3.metric(
                "💨 Wind Speed",
                f"{wind_speed} m/s"
            )

            col4.metric(
                "🌍 Pressure",
                f"{pressure} hPa"
            )

            st.divider()

            # Weather Details

            st.subheader("🌤️ Weather Details")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**City:**", weather["name"])
                st.write("**Country:**", weather["sys"]["country"])
                st.write(
                    "**Weather:**",
                    weather["weather"][0]["description"].title()
                )

            with col2:
                st.write(
                    "**Feels Like:**",
                    f"{weather['main']['feels_like']} °C"
                )
                st.write(
                    "**Minimum Temperature:**",
                    f"{weather['main']['temp_min']} °C"
                )
                st.write(
                    "**Maximum Temperature:**",
                    f"{weather['main']['temp_max']} °C"
                )

            st.divider()

            # --------------------------------
            # FORECAST DATAFRAME
            # --------------------------------

            st.subheader("📅 5-Day Weather Forecast")

            forecast_list = forecast["list"]

            data = []

            for item in forecast_list:

                data.append({
                    "Date": datetime.fromtimestamp(
                        item["dt"]
                    ),
                    "Temperature": item["main"]["temp"],
                    "Humidity": item["main"]["humidity"],
                    "Wind Speed": item["wind"]["speed"],
                    "Weather": item["weather"][0]["description"]
                })

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )

            # --------------------------------
            # TEMPERATURE CHART
            # --------------------------------

            st.subheader("📈 Temperature Analysis")

            fig1 = px.line(
                df,
                x="Date",
                y="Temperature",
                title="Temperature Forecast",
                markers=True,
                template="plotly_white"
            )

            fig1.update_layout(
                xaxis_title="Date and Time",
                yaxis_title="Temperature (°C)"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            # --------------------------------
            # HUMIDITY CHART
            # --------------------------------

            st.subheader("💧 Humidity Analysis")

            fig2 = px.area(
                df,
                x="Date",
                y="Humidity",
                title="Humidity Forecast",
                template="plotly_white"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            # --------------------------------
            # WIND SPEED CHART
            # --------------------------------

            st.subheader("💨 Wind Speed Analysis")

            fig3 = px.bar(
                df,
                x="Date",
                y="Wind Speed",
                title="Wind Speed Forecast",
                template="plotly_white"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

            # --------------------------------
            # STATISTICAL ANALYSIS
            # --------------------------------

            st.subheader("📊 Statistical Weather Analysis")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Average Temperature",
                f"{df['Temperature'].mean():.2f} °C"
            )

            col2.metric(
                "Maximum Temperature",
                f"{df['Temperature'].max():.2f} °C"
            )

            col3.metric(
                "Minimum Temperature",
                f"{df['Temperature'].min():.2f} °C"
            )

            st.write("**Average Humidity:**",
                     f"{df['Humidity'].mean():.2f}%")

            st.write("**Average Wind Speed:**",
                     f"{df['Wind Speed'].mean():.2f} m/s")

            # --------------------------------
            # DOWNLOAD CSV
            # --------------------------------

            st.divider()

            st.subheader("📥 Download Weather Report")

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Weather Data CSV",
                data=csv,
                file_name=f"{city}_weather_report.csv",
                mime="text/csv"
            )

            st.caption(
                "Data source: OpenWeatherMap API"
            )

        except requests.exceptions.RequestException as e:

            st.error(f"Network error: {e}")

        except (ValueError, KeyError, TypeError) as e:

            st.error(f"Weather analysis error: {e}")

# --------------------------------
# DEFAULT SCREEN
# --------------------------------

else:

    st.info(
        "👈 Enter your API key and city name, "
        "then click Analyze Weather."
    )

    st.markdown("""
    ### 🌍 About This Project

    The Weather Data Analyzer System is a Python-based
    web application developed using Streamlit.

    It collects real-time weather information and
    provides graphical and statistical analysis.

    **Main Modules:**
    - Real-time weather monitoring
    - Weather forecast analysis
    - Temperature visualization
    - Humidity analysis
    - Wind speed analysis
    - CSV report generation
    """)
