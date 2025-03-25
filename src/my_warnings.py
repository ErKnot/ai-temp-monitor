import json
from datetime import datetime
import time
from src.agent.tools import WritingTool, WeekAvgTempTool
from src.agent.orchestrator import AgentOrchestrator
from src.file_io import read_json_file, update_json_list, write_json_file



# from src.gemini import GeminiTempWarningMonitorAgent 



def monitor_temperature(temperature: float, lower_threshold: float, upper_threshold: float) -> str | None:
    """
    Monitors the temperature and returns a warning message if the temperature 
    is outside the specified interval.

    Args:
        temperature (float): The current temperature in °C.
        lower_threshold (float): The minimum acceptable temperature in °C.
        upper_threshold (float): The maximum acceptable temperature in °C.

    Returns:
        str | None: A warning message if the temperature is out of range, otherwise None.
    """
    if temperature < lower_threshold:
        return f"Warning: the temperature {temperature} °C is below the lower_threshold: {lower_threshold} °C."

    if temperature > upper_threshold:
        return f"Warning: the temperature {temperature} °C is abowe the upper_threshold: {upper_threshold} °C."





def check_temperature_warning(current_output: dict, lower_threshold: float, upper_threshold: float) -> dict | None:
    """
    Checks if the current temperature exceeds the defined interval and returns 
    a warning dictionary if necessary.

    Args:
        current_output (dict): A dictionary containing:
            - "temp" (float): The current temperature.
            - "ts" (datetime): The timestamp of the reading.
        lower_threshold (float): The minimum acceptable temperature.
        upper_threshold (float): The maximum acceptable temperature.

    Returns:
        dict | None: A warning dictionary containing:
            - "datetime" (str): The timestamp in ISO format.
            - "temperature" (float): The current temperature.
            - "warning_message" (str): The generated warning message.
        Returns None if the temperature is within the normal range.
    """
    monitor_message = monitor_temperature(current_output["temp"], lower_threshold, upper_threshold)
    if monitor_message:
        warning = {
                    # "datetime": current_output["ts"].isoformat(),
                    "datetime": datetime.now().isoformat(),
                    "temperature": current_output["temp"],
                    "warning_message": monitor_message
                }
        return warning

def write_agent_warnings() -> None:
    """
    Monitors a warnings log file for new warnings and generates AI-driven messages when new warnings appear.

    Parameters:
    -----------
    None

    Returns:
    --------
    None

    Raises:
    -------
    None

    Notes:
    ------
    - This function assumes the existence of the `WeatherTool`, `WritingTool`, and `AgentOrchestrator` classes.
    - It assumes that `read_json_file` and `update_json_list` are utility functions for reading from and writing to JSON files.
    - The agent message generation is currently a placeholder (`"dummy_message"`), and would need to be replaced with actual logic for invoking the orchestrator and processing the warnings.
    """
    warnings_log_list = []
    warnings_log_path = "warnings_log.json"
    llm_messages_path = "llm_messages.json"
    avg_temp_tool = WeekAvgTempTool()
    writing_tool = WritingTool()
    orchestrator = AgentOrchestrator([avg_temp_tool, writing_tool])

    time.sleep(1)

    update_warnings_log_list = read_json_file(warnings_log_path)

    # Update the wornings_log list with the new warnings and run the agent
    print("New warning messages found! We pass them to the agent...")
    warnings_log_list = update_warnings_log_list
    
    agent_message = orchestrator.run(warnings_log_list)
    # agent_message = "dummy_message"
    update_json_list(llm_messages_path, agent_message)
