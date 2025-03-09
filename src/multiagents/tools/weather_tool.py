from src.multiagents.tools.base_tool import Tool

import httpx
import os
from dotenv import load_dotenv
load_dotenv()

class WeatherTool(Tool):
    def name(self):
        return "Weather Tool"

    def description(self):
        return "Provides weather information for a given location. The payload is just the location. Example: New York"

    def use(self, location: str):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
                "q": location,
                "appid": api_key,
                "units": "metric",
                }

        response = httpx.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            response = f"The weather in {location} is currently {description} with a temperature of {temp}°C."
            return response
        else:
            return f"Sorry, I could't find weather information for {location}."
