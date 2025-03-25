from src.agent.tools.base_tool import Tool
from src.file_io import read_yaml_file
from dotenv import load_dotenv
from datetime import date, timedelta, datetime 
from typing import Generator
import httpx
import os

def daterange(start_date: date, end_date: date) -> Generator[date]:
    days = int((end_date - start_date).days)
    for day in range(days):
        yield start_date + timedelta(day)

class WeatherApiClient:
    def __init__(self, location: str):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API")
        self.url = "https://api.weatherapi.com/v1/history.json"
        self.location = location

    def get_avgtemp(self, request_date: str) -> dict:
        """Fetches the average temperature for a given date.

        Args:
            request_date (str): The date for which the average temperature is requested in 'YYYY-MM-DD' format.

        Returns:
            dict: A dictionary containing the date and average temperature in Celsius.
        """
        params = {
                "key": self.api_key,
                "q": self.location,
                "dt": request_date, 
                }

        response = httpx.get(self.url, params=params)
        data = response.json()
        response_dict = {
                "date": data["forecast"]["forecastday"][0]["date"],
                "avgtemp_c": data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
                }
        return response_dict 
    

class WeekAvgTempTool(Tool):
    """Tool to get the average temperature for the past 7 days at a specific location.

    Attributes:
        weather_api_client (WeatherApiClient): Instance of the WeatherApiClient to fetch weather data.
        config (dict): Configuration loaded from the YAML file for this tool.
    """
    def __init__(self):
        self.weather_api_client = WeatherApiClient("Brussels")
        path_config = "src/agent/config/week_avg_temp_tool.yaml"
        self.config = read_yaml_file(path_config)
        

    def name(self):
        return self.config["name"] 

    def description(self):
        return self.config["description"]

    def use(self, location: str) -> list[dict]:
        end_date = date.today()
        start_date = end_date - timedelta(days=7) 
        week_avgtemp = []
        
        for _ in daterange(start_date, end_date):
            response = self.weather_api_client.get_avgtemp(_)
            week_avgtemp.append(response)
    
        return week_avgtemp

