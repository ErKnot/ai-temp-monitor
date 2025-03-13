from src.agent.tools import WeekAvgTempTool
from datetime import date, timedelta

tool = WeekAvgTempTool()


print(tool.use("2025-01-01"))
