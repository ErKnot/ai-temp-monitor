from src.data_loader import data_preprocessing
from src.device_stream import output_stream
from src.my_warnings import check_temperature_warning, get_agent_warnings
from src.file_io import read_json_file, update_json_list, write_json_file
import asyncio

lock = asyncio.Lock()


# async def monitor_stream_and_log(device_output) -> None:
#     warnings_log = []
#     warnings_log_path = "warnings_log.json"
#
#
#     while True:
#         try:
#             current_output = next(device_output)
#         except StopIteration:
#             print("Device output exhausted. Stopping logging.")
#             return
#
#         warning = check_temperature_warning(current_output, 17., 19.8)
#         print(warning)
#
#         if warning:
#             warnings_log.append(warning)
#
#             async with lock:
#                 write_json_file(warnings_log_path, warnings_log)



async def write_warnings_log(device_output) -> None:
    warnings_log = []
    warnings_log_path = "warnings_log.json"

    while True:
        await asyncio.sleep(0.1)
        try:
            current_output = next(device_output)
        except StopIteration:
            print("Device output exhausted. Stopping logging.")
            return

        warning = check_temperature_warning(current_output, 17., 19.8)
        print(warning)

        if warning:
            warnings_log.append(warning)
            
            async with lock:
                write_json_file(warnings_log_path, warnings_log)


async def write_agent_messages():
    warnings_log_list = []
    warnings_log_path = "warnings_log.json"
    llm_messages_path = "llm_messages.json"

    while True:
        await asyncio.sleep(1)

        async with lock:
            update_warnings_log_list = read_json_file(warnings_log_path)

        if not update_warnings_log_list:
            continue
        
        # Check if there are new warnings that have not been already read. If there aren't, wait again 
        if warnings_log_list == update_warnings_log_list:
            print(f"There are no new warnings in {warnings_log_path}")
            continue
        
        # Update the wornings_log list with the new warnings
        print("New warning messages found! We pass them to the agent...")

        warnings_log_list = update_warnings_log_list
        # llm_message = get_agent_warnings(warnings_log_path)
        llm_message = "dummy message"
        update_json_list(llm_messages_path, llm_message)


async def main():
    data_path = "src/data/iot_telemetry_data.csv"
    dfs_dict = data_preprocessing(data_path, "device", "ts", "ts")
    df = dfs_dict["df1"]
    device_output = output_stream(df)
    await asyncio.gather(write_warnings_log(device_output), write_agent_messages())

asyncio.run(main())
