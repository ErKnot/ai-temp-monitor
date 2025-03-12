from src.data_preprocessing import preprocess_and_split_data
from src.device_stream import output_stream
from src.my_warnings import check_temperature_warning
from src.file_io import read_json_file, update_json_list, write_json_file
from src.agent.tools import WeatherTool, WritingTool
from src.agent.orchestrator import AgentOrchestrator

import asyncio
lock = asyncio.Lock()

import matplotlib
matplotlib.use('Qt5Agg')  # Set the backend to Qt5Agg
import matplotlib.pyplot as plt



async def graph_and_warnings(device_output) -> None:
    """Monitors temperature warnings and logs them to a JSON file."""
    warnings_log = []
    warnings_log_path = "warnings_log.json"

    # itializing the graph 
    # turning interactive mode on
    plt.ion()

    # initalizing the data queues
    temp_data = []
    ts_data = []

    # creating the cartesian plane
    fig, ax = plt.subplots(figsize=(10, 8))
    graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
    plt.ylim(10,30)
    ax.set_ylabel("Temperature (°C)")
    plt.xticks(rotation=90)

    # updating the stream, check the temperature for warning and then update the graph
    while plt.fignum_exists(fig.number):
            
        # update the stream
        try:
            current_output = next(device_output)
        except StopIteration:
            print("Device output exhausted. Stopping logging.")
            return

        # check the temperature and save it in a log file
        warning = check_temperature_warning(current_output, 17., 19.8)
        print(warning)

        if warning:
            warnings_log.append(warning)
            
            async with lock:
                write_json_file(warnings_log_path, warnings_log)

        # updating the data queues of max lenght 50
        ts_data.append(current_output["ts"])
        temp_data.append(current_output["temp"]) 
        if len(ts_data) > 50:
            ts_data.pop(0)
            temp_data.pop(0)

        graph.remove()


        graph = ax.plot(ts_data,temp_data,'b', label="Temperature (°C)")[0]
        plt.xlim(ts_data[0], ts_data[-1])

        plt.pause(0.01)

    # when closing the graph
    raise Exception

async def write_agent_messages():
    """Reads warnings and generates AI messages if new warnings appear."""
    warnings_log_list = []
    warnings_log_path = "warnings_log.json"
    llm_messages_path = "llm_messages.json"
    weather_tool = WeatherTool()
    writing_tool = WritingTool()
    orchestrator = AgentOrchestrator([weather_tool, writing_tool])

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
        
        # Update the wornings_log list with the new warnings and run the agent
        print("New warning messages found! We pass them to the agent...")
        warnings_log_list = update_warnings_log_list
        
        # agent_message = orchestrator.run(warnings_log_list)
        agent_message = "dummy_message"
        update_json_list(llm_messages_path, agent_message)



async def main():
    """Main async function to run data monitoring."""
    
    #Load the dataset and process it for the stream
    data_path = "src/data/iot_telemetry_data.csv"
    dfs_dict = preprocess_and_split_data(data_path, "device", "ts", "ts")
    df = dfs_dict["df1"]
    device_output = output_stream(df)
    
    # run the functions concurrently
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(graph_and_warnings(device_output))
            tg.create_task(write_agent_messages())
    
    # stop the program when closing the graph
    except* Exception:
        print("Bye!")

asyncio.run(main())
