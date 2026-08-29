"""
Flask Web Dashboard for Friday Weather Assistant
Provides a web interface for the weather dashboard
"""

from flask import Flask, render_template, request, jsonify
from weather_api import WeatherAPI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
api_key = os.getenv('OPENWEATHER_API_KEY')

if not api_key:
    print("Warning: OPENWEATHER_API_KEY not found in .env file")

weather_api = WeatherAPI(api_key) if api_key else None


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/api/weather/<city>')
def get_weather(city):
    """
    API endpoint to get current weather.
    
    Args:
        city (str): City name
        
    Returns:
        JSON: Weather data or error message
    """
    if not weather_api:
        return jsonify({'error': 'API key not configured'}), 400
    
    country_code = request.args.get('country', None)
    
    raw_data = weather_api.get_current_weather(city, country_code)
    weather_data = weather_api.parse_weather_data(raw_data)
    
    if 'error' in weather_data:
        return jsonify(weather_data), 400
    
    return jsonify(weather_data)


@app.route('/api/forecast/<city>')
def get_forecast(city):
    """
    API endpoint to get weather forecast.
    
    Args:
        city (str): City name
        
    Returns:
        JSON: Forecast data or error message
    """
    if not weather_api:
        return jsonify({'error': 'API key not configured'}), 400
    
    country_code = request.args.get('country', None)
    
    raw_data = weather_api.get_forecast(city, country_code)
    
    if 'error' in raw_data or 'cod' not in raw_data:
        return jsonify({'error': 'Failed to fetch forecast'}), 400
    
    # Process forecast data
    try:
        forecasts = []
        for item in raw_data.get('list', []):
            forecasts.append({
                'time': item['dt'],
                'temperature': item['main']['temp'],
                'weather': item['weather'][0]['main'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['description']
            })
        
        return jsonify({
            'city': raw_data['city']['name'],
            'country': raw_data['city']['country'],
            'forecasts': forecasts
        })
    except Exception as e:
        return jsonify({'error': f'Error processing forecast: {str(e)}'}), 400


@app.route('/api/search')
def search_weather():
    """
    Search weather for multiple cities.
    
    Returns:
        JSON: Weather data for requested cities
    """
    cities = request.args.getlist('cities')
    
    if not cities:
        return jsonify({'error': 'No cities specified'}), 400
    
    results = {}
    for city in cities:
        raw_data = weather_api.get_current_weather(city)
        weather_data = weather_api.parse_weather_data(raw_data)
        results[city] = weather_data
    
    return jsonify(results)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting Friday Weather Dashboard Flask App...")
    print("📍 Open your browser and visit: http://localhost:5000")
    app.run(debug=True, port=5000)
