from pydantic import BaseModel
import json
from src.file_io import read_yaml_file
from src.agent.llm.llm_ops import query_llm
from src.agent.logger import log_message
from termcolor import colored


class OrchestratorResponse(BaseModel):
    action: str
    input: str
    next_action: str


class AgentOrchestrator:
    """
    This class manages the orchestration of tasks, interacts with the tools,
    and uses a language model (LLM) to decide on actions based on the provided
    warnings, context, and available tools.

    Attributes:
        tools (list): A list of tool classes available for performing actions.
        memory (list): A list storing the history of responses from the orchestrator.
        max_memory (int): The maximum number of memory entries to store.
        response_format (dict): The format of the response, initialized with an empty OrchestratorResponse.
        prompt (str): The prompt template for querying the LLM, loaded from the orchestrator configuration.
        system_instruction (str): The system instruction for the LLM, loaded from the orchestrator configuration.

    Methods:
        __init__(tools: list):
            Initializes the orchestrator with the given tools and loads the prompt and system_instructions templates from the YAML file.
        
        orchestrate_task(warnings: list) -> str:
            Orchestrates a task by processing warnings, generating context, and interacting with the LLM to decide the next action.
        
        run(warnings: list) -> str:
            Runs the orchestrator in a loop, repeatedly executing tasks and checking if further actions are required.
    """
    def __init__(self, tools: list): 
        self.tools = tools
        self.memory = []
        self.max_memory = 10
        self.response_format = OrchestratorResponse(action="", input="", next_action="").model_dump()

        orch_config = read_yaml_file("src/agent/config/orchestrator.yaml")
        self.prompt = orch_config["prompt"]
        self.system_instruction= orch_config["system_instruction"]

    def orchestrate_task(self, warnings: list) -> str:
        self.memory = self.memory[-self.max_memory:]
        warnings = "\n".join(f"{warning}" for warning in warnings)
        context = "\n".join(self.memory)
        available_tools = {", ".join([f"- {tool.name()}: {tool.description()}" for tool in self.tools])}
        log_message(warnings, "WARNINGS")
        log_message(context, "CONTEXT")


        prompt = self.prompt.format(warnings=warnings, context=context, available_tools=available_tools)
        llm_response = query_llm(prompt, OrchestratorResponse, self.system_instruction)

        llm_response = json.loads(llm_response)
        log_message(llm_response, "ORCHESTRATOR")

        self.memory.append(f"Orchestrator: {llm_response}")

        action = llm_response["action"]
        input = llm_response["input"]

        if action == "respond_to_user":
            return llm_response
        for tool in self.tools:
            if tool.name() == action:
                agent_response = tool.use(input)
                print(f"{action} reponse: {agent_response}")
                self.memory.append(f"Agent Response for Task: {agent_response}")
                print(self.memory)
                return agent_response

    def run(self, warnings: list) -> str:
        while True:
            response = self.orchestrate_task(warnings)
            if isinstance(response, dict) and response["action"] == "respond_to_user":
                log_message(response["input"], "RESPONSE")
                return response["input"]
            elif response == "No action or agent needed":
                print("Response from Agent: ", response)
