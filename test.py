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

from datetime import datetime
import time

class PlotTemp:
    def __init__(self, temp_list, dates_list):
        self.temp_vals = temp_list
        self.dates_vals = dates_list

    def update_graph(self, frame):
        temp_vals = self.temp_vals[-20:]
        dates_vals = self.dates_vals[-20:]
        self.ax.set_xlim(min(dates_vals), max(dates_vals))
        self.ax.set_ylim(0,40)

        self.animate_plot.set_data(dates_vals, temp_vals)
        return self.animate_plot,
        
    async def plot(self):
        # plt.style.use("fivethirtyeight")
        self.fig, self.ax = plt.subplots()
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.35)
        self.animate_plot, = self.ax.plot([], [], lw=2)

        ani = FuncAnimation(
                fig=self.fig,
                func=self.update_graph,
                frames=100,
                interval=100
                )
        plt.show()



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

    await asyncio.sleep(1)

    async with lock:
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
        time.sleep(0.1)
        current_output = next(device_output)
        temp_list.append(current_output["temp"])
        print(temp_list)
        dates_list.append(datetime.now().isoformat())

        warning = check_temperature_warning(current_output, 17., 19.8)

        if warning:
            warnings_log.append(warning)

            write_json_file(warnings_log_path, warnings_log)

            await asyncio.to_thread(write_agent_messages)

async def stream_data_async(temp_list, dates_list, device_output):
    return await asyncio.to_thread(stream_data, temp_list, dates_list, device_output)


async def main():

    data_path = "src/data/iot_telemetry_data.csv"
    dfs_dict = preprocess_and_split_data(data_path, "device", "ts", "ts")
    df = dfs_dict["df1"]
    device_output = output_stream(df)

    temp_list = []
    dates_list = []
    
    plot = PlotTemp(temp_list, dates_list)

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(stream_data_async(temp_list, dates_list, device_output))
        task2 = tg.create_task(plot.plot())
        

asyncio.run(main())
