
import asyncio
lock = asyncio.Lock()
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
matplotlib.use("Qt5Agg")

from src.data_preprocessing import preprocess_and_split_data
from src.device_stream import output_stream
from src.my_warnings import check_temperature_warning
from src.file_io import read_json_file, update_json_list, write_json_file
from src.agent.tools import WeatherTool, WritingTool, WeekAvgTempTool
from src.agent.orchestrator import AgentOrchestrator

from datetime import datetime
import time




def write_agent_messages() -> None:
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

async def stream_data(temp_list, dates_list, device_output):
    warnings_log = []
    warnings_log_path = "warnings_log.json"
    while True:
        await asyncio.sleep(0.1)
        current_output = next(device_output)
        temp_list.append(current_output["temp"])
        print(len(temp_list))
        dates_list.append(datetime.now().isoformat())

        warning = check_temperature_warning(current_output, 17., 19.8)

        if warning:
            warnings_log.append(warning)

            async with lock:
                write_json_file(warnings_log_path, warnings_log)
            
            asyncio.create_task(asyncio.to_thread(write_agent_messages))


async def plot_temp(temp_data, ts_data):
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
    plt.ylim(10,30)
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=90)
    while plt.fignum_exists(fig.number):

        if len(ts_data) > 50:
            ts_data.pop(0)
            temp_data.pop(0)

        graph.remove()
        graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
        if len(ts_data) > 0:
            plt.xlim(ts_data[0], ts_data[-1])

        plt.pause(0.05)
        await asyncio.sleep(0.05)
        

        # fig.canvas.draw_idle()  # Non-blocking redraw
        # await asyncio.sleep(0.01)  # Yield to other tasks
    # when closing the graph
    raise Exception



async def main():

    data_path = "src/data/iot_telemetry_data.csv"
    dfs_dict = preprocess_and_split_data(data_path, "device", "ts", "ts")
    df = dfs_dict["df1"]
    device_output = output_stream(df)

    temp_list = []
    dates_list = []
    
    # plot = PlotTemp(temp_list, dates_list)
    async with asyncio.TaskGroup() as tg:
       tg.create_task(stream_data(temp_list, dates_list, device_output)) 
       tg.create_task(plot_temp( temp_list, dates_list))


asyncio.run(main())
