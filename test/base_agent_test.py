from src.agent.base_agent import Agent, AgentResponse
from src.agent.tools.weather_tool import WeatherTool

weather_tool = WeatherTool()

weather_agent = Agent(
        name = "Weather Agent",
        description = weather_tool.description(),
        tools = [weather_tool]
        )
user_input = "What is the weather in Amsterdam?"

response = weather_agent.process_input(user_input)
print(response)
print(weather_agent.memory)
