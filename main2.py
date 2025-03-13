
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

from typing import Iterator

data_path = "src/data/iot_telemetry_data.csv"
dfs_dict = preprocess_and_split_data(data_path, "device", "ts", "ts")
df = dfs_dict["df1"]
device_output = output_stream(df)
i = 0
for row in device_output:
    i += 1
    print(row)
    if i > 9:
        break

