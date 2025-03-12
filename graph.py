from src.device_stream import output_stream
# from data_streamer.data.df import separate_devices
from src.data_preprocessing import preprocess_and_split_data
import matplotlib
matplotlib.use('Qt5Agg')  # Set the backend to Qt5Agg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# generate the data stream
df_path = "src/data/iot_telemetry_data.csv"
dfs_dict = preprocess_and_split_data(df_path, "device", "ts", "ts")
df = dfs_dict["df2"]
device_output = output_stream(df)

# turning interactive mode on
plt.ion()

# inital data
temp_data = []
ts_data = []


# creating the first plot and frame
fig, ax = plt.subplots(figsize=(10, 8))
graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
plt.ylim(10,30)
ax.set_ylabel("Temperature (°C)")
plt.xticks(rotation=90)


while plt.fignum_exists(fig.number):
    current_output = next(device_output)
    ts_data.append(current_output["ts"])
    temp_data.append(current_output["temp"])

    if len(ts_data) > 50:
        ts_data.pop(0)
        temp_data.pop(0)

    graph.remove()


    graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
    plt.xlim(ts_data[0], ts_data[-1])

    plt.pause(0.01)

