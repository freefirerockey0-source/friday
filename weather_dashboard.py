"""
Weather Dashboard Module for Friday Assistant
Displays weather information in a formatted dashboard
"""

from weather_api import WeatherAPI
from typing import Dict
import os
from dotenv import load_dotenv


class WeatherDashboard:
    """
    A dashboard class to display weather information in a user-friendly format.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Weather Dashboard.

        Args:
            api_key (str): OpenWeatherMap API key
        """
        self.weather_api = WeatherAPI(api_key)

    def display_current_weather(self, city: str, country_code: str = None):
        """
        Fetch and display current weather for a city.

        Args:
            city (str): City name
            country_code (str, optional): Country code
        """
        print("\n" + "="*60)
        print("🌤️  FRIDAY WEATHER DASHBOARD - CURRENT CONDITIONS")
        print("="*60)

        raw_data = self.weather_api.get_current_weather(city, country_code)
        weather_data = self.weather_api.parse_weather_data(raw_data)

        if 'error' in weather_data:
            print(f"❌ Error: {weather_data['error']}")
            return

        print(f"\n📍 Location: {weather_data['city']}, {weather_data['country']}")
        print(f"🕐 Last Updated: {weather_data['timestamp']}")
        print("\n" + "-"*60)
        print("Temperature Information:")
        print("-"*60)
        print(f"  🌡️  Current Temperature: {weather_data['temperature']}°C")
        print(f"  🤔 Feels Like: {weather_data['feels_like']}°C")
        print(f"  💧 Humidity: {weather_data['humidity']}%")
        print(f"  🔽 Pressure: {weather_data['pressure']} hPa")
        
        print("\n" + "-"*60)
        print("Weather Conditions:")
        print("-"*60)
        print(f"  ⛅ Condition: {weather_data['weather']}")
        print(f"  📝 Description: {weather_data['weather_description'].capitalize()}")
        print(f"  ☁️  Cloudiness: {weather_data['cloudiness']}%")
        print(f"  👁️  Visibility: {weather_data['visibility']/1000:.1f} km")
        
        print("\n" + "-"*60)
        print("Wind Information:")
        print("-"*60)
        print(f"  💨 Wind Speed: {weather_data['wind_speed']} m/s")
        print(f"  🧭 Wind Direction: {weather_data['wind_direction']}°")
        
        print("\n" + "-"*60)
        print("Sun Information:")
        print("-"*60)
        print(f"  🌅 Sunrise: {weather_data['sunrise']}")
        print(f"  🌇 Sunset: {weather_data['sunset']}")
        print("\n" + "="*60 + "\n")

    def display_forecast(self, city: str, country_code: str = None):
        """
        Fetch and display 5-day weather forecast.

        Args:
            city (str): City name
            country_code (str, optional): Country code
        """
        print("\n" + "="*60)
        print("📅 FRIDAY WEATHER DASHBOARD - 5-DAY FORECAST")
        print("="*60)

        raw_data = self.weather_api.get_forecast(city, country_code)
        
        if 'error' in raw_data or 'cod' not in raw_data:
            print(f"❌ Error fetching forecast")
            return

        try:
            forecasts = raw_data.get('list', [])
            print(f"\n📍 Location: {raw_data['city']['name']}, {raw_data['city']['country']}")
            print("-"*60)

            current_date = None
            for forecast in forecasts:
                from datetime import datetime
                forecast_time = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M')
                forecast_date = forecast_time.split()[0]

                if forecast_date != current_date:
                    current_date = forecast_date
                    print(f"\n📅 {current_date}")
                    print("-"*60)

                temp = forecast['main']['temp']
                weather = forecast['weather'][0]['main']
                humidity = forecast['main']['humidity']
                wind_speed = forecast['wind']['speed']

                print(f"  {forecast_time} | {temp}°C | {weather} | 💧 {humidity}% | 💨 {wind_speed} m/s")

            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Error parsing forecast data: {str(e)}")

    def display_detailed_weather(self, city: str, country_code: str = None):
        """
        Display both current weather and forecast.

        Args:
            city (str): City name
            country_code (str, optional): Country code
        """
        self.display_current_weather(city, country_code)
        self.display_forecast(city, country_code)

    def get_weather_json(self, city: str, country_code: str = None) -> Dict:
        """
        Get weather data as JSON (useful for API responses).

        Args:
            city (str): City name
            country_code (str, optional): Country code

        Returns:
            Dict: Weather data in JSON format
        """
        raw_data = self.weather_api.get_current_weather(city, country_code)
        return self.weather_api.parse_weather_data(raw_data)

    def close(self):
        """Close the weather API session."""
        self.weather_api.close()


def main():
    """
    Main function to run the weather dashboard.
    """
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city = os.getenv('CITY', 'London')
    country_code = os.getenv('COUNTRY_CODE', 'UK')

    if not api_key:
        print("❌ Error: OPENWEATHER_API_KEY not found in .env file")
        print("Please create a .env file with your OpenWeatherMap API key")
        print("See .env.example for reference")
        return

    # Initialize and run dashboard
    dashboard = WeatherDashboard(api_key)
    
    try:
        print("\n🚀 Starting Friday Weather Dashboard...\n")
        dashboard.display_detailed_weather(city, country_code)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Friday Weather Dashboard...")
    finally:
        dashboard.close()


if __name__ == "__main__":
    main()
