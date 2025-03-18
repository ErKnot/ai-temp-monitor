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
        
    def plot(self):
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
        
        async with lock:
            write_json_file(warnings_log_path, warnings_log)

# async def stream_data_async(temp_list, dates_list, device_output):
#     return await asyncio.to_thread(stream_data, temp_list, dates_list, device_output)

async def async_plot(plot):
    """Runs the plotting function in a separate thread."""
    await asyncio.to_thread(plot.plot)

async def main():

    data_path = "src/data/iot_telemetry_data.csv"
    dfs_dict = preprocess_and_split_data(data_path, "device", "ts", "ts")
    df = dfs_dict["df1"]
    device_output = output_stream(df)

    temp_list = []
    dates_list = []
    
    plot = PlotTemp(temp_list, dates_list)

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(stream_data(temp_list, dates_list, device_output))
        task2 = tg.create_task(async_plot(plot))    

asyncio.run(main())
