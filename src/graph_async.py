import time
import asyncio
lock = asyncio.Lock()

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Qt5Agg")

async def plot_temp(ts_data: list, temp_data: list):
    """
    Plots temperature data over time in an interactive plot.

    Args:
        ts_data (list): A list of timestamps corresponding to the temperature data points.
        temp_data (list): A list of temperature values corresponding to the timestamps in `ts_data`.
        
    Raises:
        Exception: Raised when the figure is closed or when an unexpected error occurs during plotting.
    """
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.35)

    # initialize the plot
    graph = ax.plot([],[],'b')[0]
    plt.ylim(10,30)
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=90)

    # update the plot
    while plt.fignum_exists(fig.number):
        x_data = ts_data[-20:]
        y_data = temp_data[-20:]

        graph.remove()
        graph = ax.plot(ts_data,temp_data,'b')[0]

        if len(x_data) > 1:
            plt.xlim(x_data[0], x_data[-1])

        plt.pause(0.01)
        await asyncio.sleep(0.01)
        
    raise Exception
