import json
from src.gemini import AI_temp_monitor_agent



def monitor_temperature(temperature: float, lower_threshold: float, upper_threshold: float) -> str | None:
    if temperature < lower_threshold:
        return f"Warning: the temperature {temperature} °C is below the lower_threshold: {lower_threshold} °C."

    if temperature > upper_threshold:
        return f"Warning: the temperature {temperature} °C is abowe the upper_threshold: {upper_threshold} °C."




def check_temperature_warning(current_output: dict, lower_threshold: float, upper_threshold: float) -> dict | None:
    monitor_message = monitor_temperature(current_output["temp"], lower_threshold, upper_threshold)
    if monitor_message:
        warning = {
                    "datetime": current_output["ts"].isoformat(),
                    "temperature": current_output["temp"],
                    "warning_message": monitor_message
                }
        return warning



def get_agent_warnings(warnings_log_path: str) -> str:
    warnings_log_path = warnings_log_path
    
    with open(warnings_log_path, 'r') as file:
        warnings_log = json.load(file)

    agent = AI_temp_monitor_agent()
    agent.load_warnings(warnings_log)
    
    return agent.generate_content()
