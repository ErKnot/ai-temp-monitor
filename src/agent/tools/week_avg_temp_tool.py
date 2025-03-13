from src.agent.tools.base_tool import Tool
from dotenv import load_dotenv
from datetime import date, timedelta, datetime 
from textwrap import dedent
import httpx
import os

def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

class WeatherApiClient:
    def __init__(self, location: str):
        
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API")
        self.url = "https://api.weatherapi.com/v1/history.json"
        self.location = location

    def get_avgtemp(self, request_date: str):

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
    def __init__(self):
        self.weather_api_client = WeatherApiClient("Brussels")
        

    def name(self):
        return "Week Temperatur Tool"

    def description(self):
        return dedent(
                """
                Return a a place average temperature data of the last 7 days.
                It take as input the name of the place, example: "Brussels"
                """
                ) 

    def use(self, location: str):
        end_date = date.today()
        start_date = end_date - timedelta(days=7) 
        week_avgtemp = []
        # week_avgtemp = {"dates": [],
        #                 "avgtemp_c": []
        #                 } 
        
        for _ in daterange(start_date, end_date):
            response = self.weather_api_client.get_avgtemp(_)
            # week_avgtemp["dates"].append(response["date"])
            # week_avgtemp["avgtemp_c"].append(response["avgtemp_c"])
            week_avgtemp.append(response)

    
        return week_avgtemp

