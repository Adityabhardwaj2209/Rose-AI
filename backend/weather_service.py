import requests
import geocoder

class WeatherService:
    def get_current_weather(self):
        """Fetches weather based on the user's IP location."""
        try:
            # 1. Get Location via IP
            g = geocoder.ip('me')
            city = g.city or "New York" # Fallback
            
            # 2. Fetch Weather (using wttr.in for free no-key search)
            # Alternatively use OpenWeatherMap if user adds a key later
            response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
            if response.status_code == 200:
                data = response.text
                return f"Currently in {city}, it's {data}."
            return "Man, I can't reach the weather satellite right now."
        except Exception as e:
            return f"Weather error: {e}"

weather_service = WeatherService()
