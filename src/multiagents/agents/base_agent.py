
from abc import ABC, abstractmethod
import ast
import json
from pydantic import BaseModel

class AgentResponse(BaseModel):
    action: str
    args: str

class Agent:
    def __init__(self, name: str, description: str, tools: list):
        self.memory = []
        self.name = name
        self.description = description
        self.tools = tools
        self.max_memory = 10

    def json_parser(self, input_string):

        print(type(input_string))

        python_dict = ast.literal_eval(input_string)
        json_string = json.dumps(python_dict)
        json_dict = json.loads(json_string)

        if isinstance(json_dict, dict) or isinstance(json_dict, list):
            return json_dict

        raise "Invalid JSON response"

    def process_input(self, user_input):
        self.memory.append(f"User: {user_input}")

        context = "\n".join(self.memory)
        tool_descriptions = "\n".join([f"- {tool.name()}: {tool.description()}" for tool in self.tools])
        response_format =  {"action":"", "args":""} 

        prompt = f"""
        {context}

        Available tools:
        {tool_descriptions}

        Based on the user's input and context, decide if you should use a tool or respond directly.
        If you identify a action, respond with the tool name and the arguments for the tool.
        If you decide to respond directly to the user than make the action "respond_to_user" with args as you response in the following format:

        Response Format:
        {response_format}
        """

        response = query_llm(prompt, AgentResponse)
        self.memory.append(f"Agent: {response}")

        response_dict = self.json_parser(response)

        # check if any tool can handle the input

        for tool in self.tools:
            if tool.name().lower() == response_dict["action"].lower():
                return tool.use(response_dict["args"])

        return response_dict


