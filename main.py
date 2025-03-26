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


async def stream_data(temp_list: list, dates_list: list, device_output: Generator) -> None:
    """Simulate streaming data from a device, checks temperature warnings, and, whenever warnings are created, analize them with an AI agent.

    Args:
        temp_list (list): A list to store temperature data from the device output.
        dates_list (list): A list to store the corresponding timestamps of the temperature readings, created on the spot.
        device_output (Generator): A generator that yields device output, from which we get the temperature data. 

    Returns:
        None
    """
    warnings_log = []
    warnings_log_path = "warnings_log.json"

    while True:
        await asyncio.sleep(0.01)

        # generate the data and store them
        current_output = next(device_output)
        temp_list.append(current_output["temp"])
        dates_list.append(datetime.now().isoformat())

        warning = check_temperature_warning(current_output, 17., 19.8)
        
        # Start the ai agent in another thread whenever there are new warnings
        if warning:
            warnings_log.append(warning)

            async with lock:
                write_json_file(warnings_log_path, warnings_log)
            
            asyncio.create_task(asyncio.to_thread(write_agent_warnings))

        # This makes the lists two queues
        if len(temp_list) > 50:
            temp_list.pop(0)
            dates_list.pop(0)

async def main():
    """
    Asynchrounously run the function 'stream_data', that stream and check the data, and 'plot_temp', that plot the temperature datas collected. 

    Returns:
        None
    """
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
