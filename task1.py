import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import Counter

def fetch_weather_data(city, api_key, units='metric'):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={api_key}'
    response = requests.get(url)
    return response.json()

def display_weather_info(data):
    print("\n🧾 5-Day Forecast (every 3 hours):\n")

    for entry in data['list']:
        dt = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M')
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']
        wind_speed = entry['wind']['speed']
        description = entry['weather'][0]['description'].title()

        print(f"{dt} | 🌡️ Temp: {temp:.1f}°C | 💧 Humidity: {humidity}% | 🌬️ Wind: {wind_speed} m/s | ☁️ {description}")

def plot_weather(data, city):
    timestamps = []
    temperatures = []
    humidities = []
    weather_descriptions = []

    for entry in data['list']:
        timestamps.append(datetime.fromtimestamp(entry['dt']))
        temperatures.append(entry['main']['temp'])
        humidities.append(entry['main']['humidity'])
        weather_descriptions.append(entry['weather'][0]['main'])

    sns.set(style='darkgrid')

    # 🌡️ Temperature plot
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, temperatures, marker='o', color='orange', label='Temperature (°C)')
    plt.title(f'Temperature Forecast for {city.capitalize()}')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 💧 Humidity plot
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, humidities, marker='s', color='blue', label='Humidity (%)')
    plt.title(f'Humidity Forecast for {city.capitalize()}')
    plt.xlabel('Date and Time')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ☁️ Weather condition frequency
    weather_counts = Counter(weather_descriptions)
    weather_conditions = list(weather_counts.keys())
    frequencies = list(weather_counts.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=weather_conditions, y=frequencies, hue=weather_conditions, palette='muted', legend=False)
    plt.title(f'Weather Condition Frequency for {city.capitalize()}')
    plt.xlabel('Condition')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def main():
    # 🔑 Replace with your actual API key
    API_KEY = '5462fe520ef5462f92e0697d84f2412a'

    while True:
        city = input("Enter a city name (e.g., London, New York): ").strip()

        if not city:
            print("City name cannot be empty. Please try again.\n")
            continue

        print(f"\nFetching data for {city}...")

        data = fetch_weather_data(city, API_KEY)

        if 'list' not in data:
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            print("Please enter a valid city name.\n")
            continue

        # Show detailed forecast info
        display_weather_info(data)

        # Show visual plots
        plot_weather(data, city)

        break  # Exit after successful data fetch and visualization

if __name__ == "__main__":
    main()
