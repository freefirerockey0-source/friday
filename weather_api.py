"""
Weather API Module for Friday Assistant
Fetches weather data from OpenWeatherMap API
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional


class WeatherAPI:
    """
    A class to interact with OpenWeatherMap API and fetch weather data.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        """
        Initialize WeatherAPI with API key.

        Args:
            api_key (str): OpenWeatherMap API key
        """
        self.api_key = api_key
        self.session = requests.Session()

    def get_current_weather(self, city: str, country_code: Optional[str] = None) -> Dict:
        """
        Fetch current weather data for a specific city.

        Args:
            city (str): City name
            country_code (str, optional): Country code (e.g., 'US', 'UK')

        Returns:
            Dict: Weather data including temperature, conditions, humidity, etc.
        """
        location = f"{city},{country_code}" if country_code else city
        
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'  # Use Celsius
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/weather",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"Failed to fetch weather data: {str(e)}"}

    def get_forecast(self, city: str, country_code: Optional[str] = None, days: int = 5) -> Dict:
        """
        Fetch weather forecast for a specific city.

        Args:
            city (str): City name
            country_code (str, optional): Country code (e.g., 'US', 'UK')
            days (int): Number of days to forecast (max 5 for free tier)

        Returns:
            Dict: Forecast data for the next 5 days
        """
        location = f"{city},{country_code}" if country_code else city
        
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL}/forecast",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"Failed to fetch forecast data: {str(e)}"}

    def get_coordinates(self, city: str, country_code: Optional[str] = None) -> Dict:
        """
        Get latitude and longitude for a city using Geocoding API.

        Args:
            city (str): City name
            country_code (str, optional): Country code

        Returns:
            Dict: Coordinates and location details
        """
        location = f"{city},{country_code}" if country_code else city
        
        params = {
            'q': location,
            'appid': self.api_key,
            'limit': 1
        }

        try:
            response = self.session.get(
                f"{self.BASE_URL.replace('/data/2.5', '')}/geo/1.0/direct",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]
            return {'error': 'Location not found'}
        except requests.exceptions.RequestException as e:
            return {'error': f"Failed to fetch coordinates: {str(e)}"}

    @staticmethod
    def parse_weather_data(data: Dict) -> Dict:
        """
        Parse and format weather data for display.

        Args:
            data (Dict): Raw weather data from API

        Returns:
            Dict: Formatted weather data
        """
        if 'error' in data:
            return data

        try:
            weather_info = {
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'temperature': data.get('main', {}).get('temp'),
                'feels_like': data.get('main', {}).get('feels_like'),
                'humidity': data.get('main', {}).get('humidity'),
                'pressure': data.get('main', {}).get('pressure'),
                'wind_speed': data.get('wind', {}).get('speed'),
                'wind_direction': data.get('wind', {}).get('deg'),
                'cloudiness': data.get('clouds', {}).get('all'),
                'weather': data.get('weather', [{}])[0].get('main'),
                'weather_description': data.get('weather', [{}])[0].get('description'),
                'sunrise': datetime.fromtimestamp(data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(data.get('sys', {}).get('sunset', 0)).strftime('%H:%M:%S'),
                'visibility': data.get('visibility'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return weather_info
        except (KeyError, TypeError) as e:
            return {'error': f"Error parsing weather data: {str(e)}"}

    def close(self):
        """Close the requests session."""
        self.session.close()
