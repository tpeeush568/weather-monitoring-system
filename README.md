# Real-Time Weather Monitoring System

## Overview

This project is a real-time data processing system for monitoring weather conditions. It fetches data from the OpenWeatherMap API, processes it to provide summarized insights, and generates alerts based on user-configurable thresholds. The system also includes visualization of weather data.

## Features

- **Real-Time Data Retrieval:** Fetch weather data every 5 minutes for cities in India.
- **Temperature Conversion:** Converts temperature from Fahrenheit to Celsius.
- **Alerting System:** Sends email alerts when the temperature exceeds a defined threshold.
- **Daily Weather Summary:** Calculates daily aggregates for average, maximum, and minimum temperatures.
- **Visualizations:** Provides graphical representation of weather summaries, distribution of weather conditions, and temperature distribution. Each visualization is saved as an image file in the project directory.

## Requirements

- Python 3.x
- `requests`
- `schedule`
- `pandas`
- `matplotlib`
- `seaborn`
- `python-dotenv`
- `configparser`

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/tpeeush568/weather-monitoring-system.git
   cd weather-monitoring-system
2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Set up the Environment Variables:**

    Copy the .env.example to .env and update with your credentials:
    ```bash
    cp .env.example .env 
    ```
    Update .env with your OpenWeatherMap API key and SMTP server configuration.

5. **Iniatialize Database**

    Run the weather_data.py script to set up the database and start fetching data:
    ```bash
    python weather_data.py
    ```
6. **Start Data Processing**

    Run the data_processing.py script to calculate daily weather summaries:
    ```bash
    python data_processing.py
    ```
7. **Visualize Data**

    Run the visualization.py script to generate visualizations:
    ```bash
    python visualization.py
    ```
    Each visualization will be saved as an image file in the project directory.

**Note:** Keep the weather_data.py script running continuously to ensure that data is fetched and updated in real-time. You can run it in a separate terminal or background process.

## Configuration

- **OpenWeatherMap API Key:** Update the `OPENWEATHERMAP_API_KEY` in the `.env` file.

    To obtain an API key:
    1. Visit [OpenWeatherMap](https://openweathermap.org/).
    2. Sign up for an account or log in.
    3. Navigate to the API section and subscribe to the free plan (or a suitable plan for your needs).
    4. Copy your API key from the API keys section and paste it into the `.env` file.

- **SMTP Server Configuration:** Configure the SMTP server settings in the `.env` file for sending email alerts.

- **Temperature Threshold:** Set the temperature threshold in the `config.ini` file for triggering alerts.
