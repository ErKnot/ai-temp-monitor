
import asyncio
import matplotlib.pyplot as plt
import random
from typing import Dict

async def data_stream(queue: asyncio.Queue):
    """Simulates a continuous data stream and puts data into a queue."""
    ts = 0
    while True:
        data = {"ts": ts, "temp": random.uniform(15, 25)}
        await queue.put(data)  # Send data to consumers
        ts += 1
        await asyncio.sleep(1)  # Simulate real-time delay

async def plot_graph(queue: asyncio.Queue):
    """Continuously updates the graph with incoming data from the queue."""
    plt.ion()  # Turn on interactive mode

    temp_data, ts_data = [], []
    fig, ax = plt.subplots(figsize=(10, 8))
    graph, = ax.plot(ts_data, temp_data, 'b', label="Temperature (°C)")
    ax.set_ylabel("Temperature (°C)")

    while plt.fignum_exists(fig.number):  # Stop when the graph is closed
        data = await queue.get()  # Get new data from the queue
        ts_data.append(data["ts"])
        temp_data.append(data["temp"])

        if len(ts_data) > 50:
            ts_data.pop(0)
            temp_data.pop(0)

        graph.set_xdata(ts_data)
        graph.set_ydata(temp_data)
        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw_idle()  # Non-blocking redraw
        await asyncio.sleep(0.01)  # Yield to other tasks

async def check_data(queue: asyncio.Queue):
    """Checks data every 10 seconds."""
    while True:
        await asyncio.sleep(10)  # Wait 10 seconds
        print("Checking data...")
        if queue.empty():
            print("No new data.")
            continue

        data = await queue.get()
        print(f"Checked Data: {data}")

async def main():
    """Runs the stream, graph, and checker concurrently."""
    queue = asyncio.Queue()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(data_stream(queue))
        tg.create_task(plot_graph(queue))
        tg.create_task(check_data(queue))

asyncio.run(main())
