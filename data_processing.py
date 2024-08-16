import sqlite3

def calculate_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            city, 
            DATE(timestamp) as date, 
            AVG(temp) as avg_temp, 
            MAX(temp) as max_temp, 
            MIN(temp) as min_temp, 
            weather
        FROM weather
        GROUP BY city, date
    ''')
    summaries = cursor.fetchall()
    conn.close()

    for summary in summaries:
        city, date, avg_temp, max_temp, min_temp, weather = summary
        print(f"Daily Summary for {date} in {city}:")
        print(f"Average Temperature: {avg_temp:.2f}°C")
        print(f"Maximum Temperature: {max_temp:.2f}°C")
        print(f"Minimum Temperature: {min_temp:.2f}°C")
        print(f"Dominant Weather Condition: {weather}")
        print("----------------------------------------")

if __name__ == "__main__":
    calculate_daily_summary()
