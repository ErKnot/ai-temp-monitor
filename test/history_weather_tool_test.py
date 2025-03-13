from src.agent.tools.history_weather_tool import HistoryWeatherTool, WeatherApiClient, daterange
from datetime import date, timedelta

h_w_tool = HistoryWeatherTool()

print(h_w_tool.use())
