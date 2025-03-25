import json
import yaml
import os

def read_json_file(file_path: str) -> dict|list|None:
    """Check if a json file exists. If it does, return its content."""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return None

    with open(file_path, "r") as file:
        return json.load(file)

def write_json_file(file_path: str, content) -> None:
    """Create a json file and write the content in it."""
    with open(file_path, "w") as file:
        json.dump(content, file, indent=4)


def update_json_list(file_path: str, content: str) -> None:
    """Update the list in a json file. If the file does not exists, it creates one."""
    if not os.path.exists(file_path):
        print(f"Creating the file {file_path}...")
        with open(file_path, "w") as file:
            json.dump([content], file, indent=4)
    
    else:
        with open(file_path, "r+") as file:
            print(f"Updating the file {file_path}...")
            contents_list = json.load(file)
            contents_list.append(content)
            file.seek(0)
            json.dump(contents_list, file, indent=4)


def read_yaml_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return None
    
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
