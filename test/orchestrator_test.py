from src.agent.orchestrator import OrchestratorResponse, AgentOrchestrator 
from src.agent.tools.weather_tool import WeatherTool
from src.agent.tools.writing_tool import WritingTool
from src.file_io import read_json_file

# weather_tool = WeatherTool()
#
# writing_tool = WritingTool()
# agent_orch = AgentOrchestrator([weather_tool, writing_tool])

path = "test/mockwarnings_log.json"
warnings = read_json_file(path)
print(type(warnings))
print(warnings)
# agent_orch.run(warnings)
