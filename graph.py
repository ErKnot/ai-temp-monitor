import asyncio
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
matplotlib.use("Qt5Agg")

from src.data_preprocessing import preprocess_and_split_data
from src.device_stream import output_stream

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




def stream_data(temp_list, dates_list, device_output):
    while True:
        current_output = next(device_output)
        temp_list.append(current_output["temp"])
        print(temp_list)
        dates_list.append(datetime.now().isoformat())
        time.sleep(0.1)

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
    # await asyncio.gather(stream_data_async(temp_list, dates_list, device_output),
    #                      plot.plot()
    #                      )
        

asyncio.run(main())
