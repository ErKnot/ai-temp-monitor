import httpx
import os
from dotenv import load_dotenv
load_dotenv()
from src.singleagent.tools.weather_tool import WeatherTool



api_key = os.getenv("OPENWEATHER_API_KEY")
weather_tool = WeatherTool()
print("Name of the Tool: ", weather_tool.name())
print("Descriptio of the Tool:", weather_tool.description())
print(weather_tool.use("London"))
