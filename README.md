# 🌤️ Friday - AI Weather Assistant

Friday is a Python-based weather assistant inspired by Tony Stark's AI from Iron Man. It provides real-time weather data, forecasts, and a beautiful dashboard interface.

## Features

- ✅ **Current Weather Data** - Get real-time weather information for any city
- ✅ **5-Day Forecast** - View detailed weather forecasts
- ✅ **Web Dashboard** - Beautiful Flask-based web interface
- ✅ **REST API** - JSON API endpoints for integration
- ✅ **Command-Line Interface** - Direct CLI access to weather data
- ✅ **Multiple Locations** - Search weather for multiple cities
- ✅ **Detailed Information** - Temperature, humidity, wind speed, visibility, sunrise/sunset times

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/freefirerockey0-source/friday.git
   cd friday
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get an API Key**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key from your account dashboard

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   CITY=London
   COUNTRY_CODE=UK
   ```

## Usage

### Command Line Dashboard

Run the terminal-based weather dashboard:

```bash
python weather_dashboard.py
```

Output example:
```
============================================================
🌤️  FRIDAY WEATHER DASHBOARD - CURRENT CONDITIONS
============================================================

📍 Location: London, GB
🕐 Last Updated: 2024-08-29 14:35:22

------------------------------------------------------------
Temperature Information:
------------------------------------------------------------
  🌡️  Current Temperature: 22.5°C
  🤔 Feels Like: 21.8°C
  💧 Humidity: 65%
  🔽 Pressure: 1013 hPa
```

### Web Dashboard

Start the Flask web application:

```bash
python flask_app.py
```

Then open your browser and visit: **http://localhost:5000**

Features:
- 🎨 Modern, responsive UI
- 🔍 Search weather for any city
- 📊 Detailed weather metrics
- ⚡ Real-time updates
- 📱 Mobile-friendly design

### Python API Integration

Use Friday in your own Python projects:

```python
from weather_api import WeatherAPI

# Initialize the API
api = WeatherAPI(api_key="your_api_key")

# Get current weather
weather_data = api.get_current_weather("London", "UK")
parsed_data = api.parse_weather_data(weather_data)

print(f"Current temperature: {parsed_data['temperature']}°C")
print(f"Condition: {parsed_data['weather_description']}")

# Get forecast
forecast_data = api.get_forecast("London", "UK", days=5)

api.close()
```

### REST API Endpoints

If running the Flask app, you can use these API endpoints:

#### Get Current Weather
```bash
GET /api/weather/<city>?country=<country_code>
```
Example:
```bash
curl "http://localhost:5000/api/weather/London?country=UK"
```

Response:
```json
{
  "city": "London",
  "country": "GB",
  "temperature": 22.5,
  "feels_like": 21.8,
  "humidity": 65,
  "pressure": 1013,
  "wind_speed": 4.5,
  "weather": "Partly cloudy",
  "weather_description": "partly cloudy"
}
```

#### Get 5-Day Forecast
```bash
GET /api/forecast/<city>?country=<country_code>
```

#### Search Multiple Cities
```bash
GET /api/search?cities=London&cities=Paris&cities=Tokyo
```

## Project Structure

```
friday/
├── weather_api.py          # OpenWeatherMap API wrapper
├── weather_dashboard.py    # CLI dashboard
├── flask_app.py            # Web application
├── templates/
│   └── index.html          # Web UI
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## File Descriptions

### weather_api.py
- `WeatherAPI` class - Handles all API calls to OpenWeatherMap
- `get_current_weather()` - Fetches current weather conditions
- `get_forecast()` - Fetches 5-day weather forecast
- `get_coordinates()` - Gets latitude/longitude for a location
- `parse_weather_data()` - Formats raw API data for display

### weather_dashboard.py
- `WeatherDashboard` class - Terminal-based weather display
- `display_current_weather()` - Shows current conditions in formatted output
- `display_forecast()` - Shows 5-day forecast
- `display_detailed_weather()` - Shows both current and forecast
- `get_weather_json()` - Returns weather data as JSON

### flask_app.py
- Flask web application with REST API
- Routes for current weather, forecast, and search
- Error handling and JSON responses

### templates/index.html
- Beautiful, responsive web dashboard
- Real-time weather search
- Weather card display
- Mobile-friendly design

## Dependencies

- **requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **flask** - Web framework

## Weather Data Provided

Friday provides the following information:

- **Temperature** - Current temperature and "feels like" temperature
- **Humidity** - Percentage of air moisture
- **Pressure** - Atmospheric pressure in hPa
- **Wind** - Wind speed and direction
- **Clouds** - Cloud coverage percentage
- **Visibility** - Visibility distance in meters
- **Sunrise/Sunset** - Times for sun rise and set
- **Weather Condition** - Clear, Cloudy, Rainy, Snowy, etc.
- **Description** - Detailed weather description

## Configuration

Edit `.env` file to customize:

```
OPENWEATHER_API_KEY=your_api_key    # Required: OpenWeatherMap API key
CITY=London                         # Default city for CLI
COUNTRY_CODE=UK                     # Default country code
```

## Troubleshooting

### API Key Issues
- **Error: "API key not found"** - Ensure you've created a `.env` file and added your API key
- **Error: "Invalid API key"** - Verify your API key is correct on OpenWeatherMap

### Weather Not Found
- Use the full city name (e.g., "New York" instead of "NY")
- Add country code for better accuracy (e.g., "London,UK")

### Connection Issues
- Check your internet connection
- Verify OpenWeatherMap API is accessible
- Check API rate limits (free tier has limits)

## Future Enhancements

- 🔔 Weather alerts and notifications
- 📊 Weather history and analytics
- 🗺️ Weather maps and radar
- 💬 Natural language queries ("What's the weather like tomorrow?")
- 🌍 Multi-language support
- 📲 Mobile app version

## API Rate Limits

Free tier OpenWeatherMap API has:
- **Calls per minute:** 60
- **Calls per month:** 1,000,000

For production use, consider upgrading your plan.

## License

This project is released without a specific license. Feel free to use and modify the code as needed.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review OpenWeatherMap API documentation
3. Open an issue on GitHub

---

**Created with ❤️ by Friday - Tony Stark's AI Assistant**
