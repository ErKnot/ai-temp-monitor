
from src.data_preprocessing import preprocess_and_split_data
from src.device_stream import output_stream
from src.my_warnings import check_temperature_warning
from src.file_io import read_json_file, update_json_list, write_json_file
from src.agent.tools import WeatherTool, WritingTool, WeekAvgTempTool
from src.agent.orchestrator import AgentOrchestrator

import asyncio
lock = asyncio.Lock()

import matplotlib
matplotlib.use('Qt5Agg')  # Set the backend to Qt5Agg
import matplotlib.pyplot as plt

from datetime import datetime
from typing import Iterator


async def write_agent_messages() -> None:
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
    # weather_tool = WeatherTool()
    avg_temp_tool = WeekAvgTempTool()
    writing_tool = WritingTool()
    orchestrator = AgentOrchestrator([avg_temp_tool, writing_tool])

    await asyncio.sleep(10)

    async with lock:
        warnings_log_list = read_json_file(warnings_log_path)

    agent_message = orchestrator.run(warnings_log_list)
    # agent_message = "dummy_message"
    update_json_list(llm_messages_path, agent_message)

async def stream_and_log_warnings():


    warnings_log = []
    warnings_log_path = "warnings_log.json"

    try:
        current_output = next(device_output)
    except StopIteration:
        print("Device output exhausted. Stopping logging.")
        return

    # check the temperature and save it in a log file
    warning = check_temperature_warning(current_output, 17., 19.8)
    print(warning)

    if warning:
        warnings_log.append(warning)
        
        async with lock:
            write_json_file(warnings_log_path, warnings_log)

        asyncio.create_task(write_agent_messages())
