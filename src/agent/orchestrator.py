from pydantic import BaseModel
import json
from src.agent.llm.llm_ops import query_llm
from src.agent.logger import log_message
from termcolor import colored


class OrchestratorResponse(BaseModel):
    action: str
    input: str
    next_action: str

class AgentOrchestrator:
    def __init__(self, tools: list): 
        self.tools = tools
        self.memory = []
        self.max_memory = 10
        self.response_format = OrchestratorResponse(action="", input="", next_action="").model_dump()

    def orchestrate_task(self, warnings):
        self.memory = self.memory[-self.max_memory:]
        warnings = "\n".join(f"{warning}" for warning in warnings)
        context = "\n".join(self.memory)


        print(colored(f"WARNING:\n{warnings}","red"))
        print(colored(f"CONTEXT:\n{context}", "blue"))

        # response_format = OrchestratorResponse(action="", input="", next_action="").model_dump()

        prompt=f"""
You are an AI Orchestrator responsible for gathering the necessary information for analyzing warning messages.
You have access to multiple tools to assist in your investigation. Your goal is to provide the Writing Tool with as much relevant information as possible. 
You will be provided with the warnings to analyzen, a context that tracks previous actions and the tools you can use.

### Warnings ###
{warnings}

### Context ###
{context}

### Available Tools ###
{", ".join([f"- {tool.name()}: {tool.description()}" for tool in self.tools])}

### Guidelines ###
- Some tasks may require multiple agents.
- The original user input could contain multiple tasks.
- Use the context to understand previous actions taken.
- Read the context carefully before selecting the next step.
- If no further action is required, set `action = "respond_to_user"` and as 'input' copy the response ot the Writing Tool. 
- If you decide to use a tool you will return the tool name in the form of {self.response_format}

```json
{json.dumps(self.response_format, indent=2)}"""

#         prompt=f"""
# You are an AI Orchestrator responsible for analyzing warnings and diagnosing possible causes. 
# You have access to multiple tools to assist in your investigation. Your goal is to interpret the warnings, 
# identify the most likely root causes, and use the appropriate tools to gather more information. 
# You will be provided with warnings to analyzen, a context that tracks previous actions and the tools you can use.
#
# ### Warnings ###
# {warnings}
#
# ### Context ###
# {context}
#
# ### Available Tools ###
# {", ".join([f"- {tool.name()}: {tool.description()}" for tool in self.tools])}
#
# ### Guidelines ###
# - Some tasks may require multiple agents.
# - The original user input could contain multiple tasks.
# - Use the context to understand previous actions taken.
# - Read the context carefully before selecting the next step.
# - If no further action is required, set `action = "respond_to_user"` and summarize findings.
# - If you decide to use a tool you will return the tool name in the form of {self.response_format}
#
# ```json
# {json.dumps(self.response_format, indent=2)}"""
        
        llm_response = query_llm(prompt, OrchestratorResponse)

        llm_response = json.loads(llm_response)
        print(colored(f"LLM Response:\n{llm_response}", "yellow"))

        self.memory.append(f"Orchestrator: {llm_response}")

        action = llm_response["action"]
        input = llm_response["input"]

        print(f"Action identified by LLM: {action}")

        if action == "respond_to_user":
            return llm_response
        for tool in self.tools:
            if tool.name() == action:
                agent_response = tool.use(input)
                print(f"{action} reponse: {agent_response}")
                self.memory.append(f"Agent Response for Task: {agent_response}")
                print(self.memory)
                return agent_response

    def run(self, warnings):
        while True:
            response = self.orchestrate_task(warnings)
            print(colored(f"Final response of orchestrator:\n{response}", "magenta"))
            if isinstance(response, dict) and response["action"] == "respond_to_user":
                log_message(f"Reponse from Agent: {response["input"]}", "RESPONSE")
                return response["input"]
            elif response == "No action or agent needed":
                print("Response from Agent: ", response)
