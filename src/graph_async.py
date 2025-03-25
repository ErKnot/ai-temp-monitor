import time
import asyncio
lock = asyncio.Lock()

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Qt5Agg")

async def plot_temp(ts_data: list, temp_data: list):
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.35)
    graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
    plt.ylim(10,30)
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=90)
    while plt.fignum_exists(fig.number):
        x_data = ts_data[-20:]
        y_data = temp_data[-20:]

        graph.set_data(x_data, y_data)
        # graph.remove()
        # graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]

        if len(x_data) > 1:
            plt.xlim(x_data[0], x_data[-1])

        plt.draw()
        plt.pause(0.05)
        await asyncio.sleep(0.05)
        
    raise Exception
