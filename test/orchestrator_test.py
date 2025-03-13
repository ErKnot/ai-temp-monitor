from src.agent.orchestrator import OrchestratorResponse, AgentOrchestrator 
from src.agent.tools import WritingTool, WeekAvgTempTool
from src.file_io import read_json_file

# weather_tool = WeatherTool()
#
week_avgtemp_tool = WeekAvgTempTool()
writing_tool = WritingTool()
agent_orch = AgentOrchestrator([week_avgtemp_tool, writing_tool])

path = "warnings_log.json"
warnings = read_json_file(path)
print(type(warnings))
print(warnings)
agent_orch.run(warnings)
