from termcolor import colored

def log_message(message: str, level: str):
    if level == "REASON":
        print(colored("REASON: " + message, "blue"))
    elif level == "ACTION":
        print(colored("ACTION: " + message, "yellow"))
    elif level == "error":
        print(colored("ERROR: " + message, "red"))
    elif level == "RESPONSE":
        print(colored("RESPONSE: " + message, "green"))
