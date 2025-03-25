import asyncio
lock = asyncio.Lock()

from src.data_preprocessing import preprocess_and_split_data
from src.device_stream import output_stream
from src.my_warnings import check_temperature_warning, write_agent_warnings
from src.file_io import read_json_file, update_json_list, write_json_file
from src.graph_async import plot_temp

from datetime import datetime
import time

from typing import Generator


async def stream_data(temp_list: list, dates_list: list, device_output: Generator):
    warnings_log = []
    warnings_log_path = "warnings_log.json"
    while True:
        await asyncio.sleep(0.01)
        current_output = next(device_output)
        temp_list.append(current_output["temp"])
        print(len(temp_list))
        dates_list.append(datetime.now().isoformat())

        warning = check_temperature_warning(current_output, 17., 19.8)

        if warning:
            warnings_log.append(warning)

            async with lock:
                write_json_file(warnings_log_path, warnings_log)
            
            asyncio.create_task(asyncio.to_thread(write_agent_warnings))

async def main():

    data_path = "src/data/iot_telemetry_data.csv"
    dfs_dict = preprocess_and_split_data(data_path, "device", "ts", "ts")
    df = dfs_dict["df1"]
    device_output = output_stream(df)

    temp_list = []
    dates_list = []
    
    async with asyncio.TaskGroup() as tg:
       tg.create_task(stream_data(temp_list, dates_list, device_output)) 
       tg.create_task(plot_temp(dates_list, temp_list))


asyncio.run(main())
