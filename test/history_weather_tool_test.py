from src.agent.tools.history_weather_tool import HistoryWeatherTool

h_w_t = HistoryWeatherTool()
print(h_w_t.name())
print(h_w_t.description())
print(h_w_t.use("Brussels"))
