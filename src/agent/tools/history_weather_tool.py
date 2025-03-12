from src.agent.tools.base_tool import Tool
from dotenv import load_dotenv
from datetime import date, timedelta
from textwrap import dedent
import httpx
import os


class HistoryWeatherTool(Tool):
    def name(self):
        return "Hystory weather tool"

    def description(self):
        return dedent(
                """
                Return a location history weather information of the last 7 days.
                It take as input the name of the place, example: "Brussels"
                """
                ) 

    def use(self, location: str):
        request_date = date.today() - timedelta(days=7) 
        load_dotenv()
        api_key = os.getenv("WEATHER_API")
        url = "https://api.weatherapi.com/v1/history.json"
        params = {
                "key": api_key,
                "q": location,
                "dt": request_date
                }

        response = httpx.get(url, params=params)
        data = response.json()
        print(data)
        


