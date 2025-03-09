from src.singleagent.tools.base_tool import Tool
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

class WeatherTool(Tool):
    def name(self):
        return "Weather Tool"

    def description(self):
        return "Proides weather informatio for a given location. The payload is just the location. Example: New York"

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


if __name__ == "__main__":
    weather_tool = WeatherTool()

    print("Name of the Tool: ", weather_tool.name())
    print("Descriptio of the Tool:", weather_tool.description())

