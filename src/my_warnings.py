import json
# from src.gemini import GeminiTempWarningMonitorAgent 



def monitor_temperature(temperature: float, lower_threshold: float, upper_threshold: float) -> str | None:
    """
    Monitors the temperature and returns a warning message if the temperature 
    is outside the specified interval.

    Args:
        temperature (float): The current temperature in °C.
        lower_threshold (float): The minimum acceptable temperature in °C.
        upper_threshold (float): The maximum acceptable temperature in °C.

    Returns:
        str | None: A warning message if the temperature is out of range, otherwise None.
    """
    if temperature < lower_threshold:
        return f"Warning: the temperature {temperature} °C is below the lower_threshold: {lower_threshold} °C."

    if temperature > upper_threshold:
        return f"Warning: the temperature {temperature} °C is abowe the upper_threshold: {upper_threshold} °C."





def check_temperature_warning(current_output: dict, lower_threshold: float, upper_threshold: float) -> dict | None:
    """
    Checks if the current temperature exceeds the defined interval and returns 
    a warning dictionary if necessary.

    Args:
        current_output (dict): A dictionary containing:
            - "temp" (float): The current temperature.
            - "ts" (datetime): The timestamp of the reading.
        lower_threshold (float): The minimum acceptable temperature.
        upper_threshold (float): The maximum acceptable temperature.

    Returns:
        dict | None: A warning dictionary containing:
            - "datetime" (str): The timestamp in ISO format.
            - "temperature" (float): The current temperature.
            - "warning_message" (str): The generated warning message.
        Returns None if the temperature is within the normal range.
    """
    monitor_message = monitor_temperature(current_output["temp"], lower_threshold, upper_threshold)
    if monitor_message:
        warning = {
                    "datetime": current_output["ts"].isoformat(),
                    "temperature": current_output["temp"],
                    "warning_message": monitor_message
                }
        return warning



def get_agent_warnings(warnings_log_path: str) -> str:
    """
    Loads warnings from a log file and generates AI-generated messages 
    using the GeminiTempWarningMonitorAgent.

    Args:
        warnings_log_path (str): The file path to the warnings log (JSON format).

    Returns:
        str: The AI-generated warning content.
    """
    warnings_log_path = warnings_log_path
    
    with open(warnings_log_path, 'r') as file:
        warnings_log = json.load(file)

    agent = GeminiTempWarningMonitorAgent()
    agent.load_warnings(warnings_log)
    
    return agent.generate_content()
