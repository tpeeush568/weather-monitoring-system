import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import seaborn as sns

def fetch_data():
    conn = sqlite3.connect('weather_data.db')
    query = '''
    SELECT city, temp, feels_like, timestamp, weather
    FROM weather
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_daily_summary(df):
    # Convert timestamp to datetime and extract date
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Ensure required columns are present
    if 'date' not in df.columns or 'temp' not in df.columns:
        raise KeyError("Required columns are missing from the DataFrame")

    # Group by date and calculate aggregates
    daily_summary = df.groupby('date').agg({
        'temp': ['mean', 'max', 'min'],
        'weather': lambda x: x.mode()[0]  # Most frequent weather condition
    }).reset_index()

    daily_summary.columns = ['date', 'average_temp', 'max_temp', 'min_temp', 'dominant_weather']

    # Plot daily summary
    plt.figure(figsize=(12, 6))
    plt.plot(daily_summary['date'], daily_summary['average_temp'], label='Average Temperature', marker='o')
    plt.plot(daily_summary['date'], daily_summary['max_temp'], label='Maximum Temperature', marker='o')
    plt.plot(daily_summary['date'], daily_summary['min_temp'], label='Minimum Temperature', marker='o')
    
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Weather Summary')
    plt.legend()
    plt.grid(True)
    
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    
    plt.savefig('daily_summary.png')
    plt.show()

def plot_weather_distribution(df):
    # Ensure 'city' and 'weather' columns exist
    if 'city' not in df.columns or 'weather' not in df.columns:
        raise KeyError("City or weather column is missing from the DataFrame")

    # Plot distribution of weather conditions
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='weather', order=df['weather'].value_counts().index)
    
    plt.xlabel('Weather Condition')
    plt.ylabel('Count')
    plt.title('Weather Condition Distribution')
    plt.grid(True)
    
    plt.savefig('weather_distribution.png')
    plt.show()

def plot_temperature_distribution(df):
    # Ensure 'temp' column exists
    if 'temp' not in df.columns:
        raise KeyError("Temperature column is missing from the DataFrame")

    plt.figure(figsize=(12, 6))
    sns.histplot(df['temp'], bins=30, kde=True)
    
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.title('Temperature Distribution')
    plt.grid(True)
    
    plt.savefig('temperature_distribution.png')
    plt.show()

def main():
    df = fetch_data()
    if not df.empty:
        plot_daily_summary(df)
        plot_weather_distribution(df)
        plot_temperature_distribution(df)
    else:
        print("No data available for visualization.")

if __name__ == "__main__":
    main()
