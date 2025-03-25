from termcolor import colored

def log_message(message: str, level: str):
    if level == "WARNINGS":
        print(colored(f"WARNINGS:\n{message}", "red"))
    elif level == "CONTEXT":
        print(colored(f"CONTEXT:\n{message}", "blue"))
    elif level == "ORCHESTRATOR":
        print(colored(f"ORCHESTRATOR RESPONSE:\n{message}", "yellow"))
    elif level == "RESPONSE":
        print(colored("RESPONSE:\n" + message, "green"))
