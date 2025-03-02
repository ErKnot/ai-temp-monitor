from data_streamer.device_output import output_stream
from data_streamer.data.df import separate_devices
import matplotlib
matplotlib.use('Qt5Agg')  # Set the backend to Qt5Agg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# initial data
temp_data = []
ts_data = []

# creating the first plot and frame
fig, ax = plt.subplots(figsize=(10, 8))
graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
plt.ylim(10,30)
ax.set_ylabel("Temperature (°C)")
plt.xticks(rotation=90)

# generate the data stream
dfs_dict = separate_devices()
df = dfs_dict["df2"]
device_output = output_stream(df)

# updates the data and graph
def update(frame):
    global graph

    current_output = next(device_output)

    # updating the data
    ts_data.append(current_output["ts"])
    temp_data.append(current_output["temp"])

    if len(ts_data) > 50:
        ts_data.pop(0)
        temp_data.pop(0)

    # creating a new graph or updating the graph
    graph.set_xdata(ts_data)
    graph.set_ydata(temp_data)
    plt.xlim(ts_data[0], ts_data[-1])

anim = FuncAnimation(fig, update, frames = None, interval=10)
plt.show()
