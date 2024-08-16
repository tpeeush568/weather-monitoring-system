import requests  # type: ignore
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv  # type: ignore
import schedule
import time
from alerting import send_email  # Import the send_email function from alerting.py

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('OPENWEATHERMAP_API_KEY')
base_url = "http://api.openweathermap.org/data/2.5/weather"
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
alert_threshold = 35  # Temperature threshold for alert in Celsius

# Temperature conversion function
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0 / 9.0

def fetch_weather_data(city):
    url = f"{base_url}?q={city}&units=imperial&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def process_weather_data(city, data):
    if data:
        weather_condition = data['weather'][0]['main'].lower()
        temp_fahrenheit = data['main']['temp']
        feels_like_fahrenheit = data['main']['feels_like']
        timestamp = data['dt']
        dt = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        temp_celsius = fahrenheit_to_celsius(temp_fahrenheit)
        feels_like_celsius = fahrenheit_to_celsius(feels_like_fahrenheit)

        print(f"Weather in {city}:")
        print(f"Weather Condition: {weather_condition}")
        print(f"Temperature: {temp_fahrenheit}°F / {temp_celsius:.2f}°C")
        print(f"Feels Like: {feels_like_fahrenheit}°F / {feels_like_celsius:.2f}°C")
        print(f"Data retrieved at (UTC): {dt}")

        return {
            'city': city,
            'weather': weather_condition,
            'temp': temp_celsius,
            'feels_like': feels_like_celsius,
            'timestamp': dt
        }
    return None

def store_weather_data(data):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            weather TEXT,
            temp REAL,
            feels_like REAL,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO weather (city, weather, temp, feels_like, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['city'], data['weather'], data['temp'], data['feels_like'], data['timestamp']))
    conn.commit()
    conn.close()

def check_alerts(data):
    if data['temp'] > alert_threshold:
        alert_message = f"Alert! The temperature in {data['city']} has exceeded the threshold of {alert_threshold}°C."
        print(alert_message)
        send_email(alert_message)  # Call the function to send an email alert

def update_weather():
    for city in cities:
        weather_data = fetch_weather_data(city)
        processed_data = process_weather_data(city, weather_data)
        if processed_data:
            store_weather_data(processed_data)
            check_alerts(processed_data)

def main():
    # Schedule the weather update every 5 minutes
    schedule.every(5).minutes.do(update_weather)

    print("Scheduler started. Press Ctrl+C to stop.")
    
    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
