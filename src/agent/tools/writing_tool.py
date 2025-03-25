from textwrap import dedent
import json
from src.file_io import read_yaml_file 
from src.agent.tools.base_tool import Tool
from src.agent.llm.llm_ops import query_llm
from pydantic import BaseModel

class WritingToolResponse(BaseModel):
    message: str

class WritingTool(Tool):
    def __init__(self):
        path_config = "src/agent/config/writing_tool.yaml"
        self.config = read_yaml_file(path_config)

    def name(self) -> str:
        # return "Writing Tool"
        return self.config["name"]

    def description(self) -> str:
        return self.config["description"]

    def use(self, prompt: str) -> str:
        prompt = self.config["prompt"].format(prompt=prompt)
        llm_response = query_llm(prompt, WritingToolResponse, self.config["system_instruction"] )
        llm_response = json.loads(llm_response) 

        return llm_response["message"]
