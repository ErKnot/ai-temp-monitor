import ast
import json
from src.multiagents.agents.base_agent import Agent
from src.multiagents.llm.llm_ops import query_llm
from src.multiagents.tools.weather_tool import WeatherTool
from logger import log_message
from pydantic import BaseModel


class OrchestratorResponse(BaseModel):
    action: str
    input: str
    next_action: str

class AgentOrchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = agents
        self.memory = []
        self.max_memory = 10

    # def json_parser(self, input_string: str):
    #     # Since it is possible to define genai output string format, I probably just need a function that extract a json from a string
    #     pass

    def orchestrate_tasks(self, warning_messages_log):
        # The orchestrator is designd to handle a string. I should change it to handle a list: warning_messages_log
        self.memory = self.memory[-self.max_memory:]

        context = "\n".join(self.memory)
        print(f"Context: {context}")

        response_format = OrchestratorResponse(action="", input="", next_action="").model_dump()

        def get_prompt(warning_messages_log):
            return f"""
                Use the context from memory to plan next steps.
                Context:
                    {context}

                You are an expert in handling error messages and understanding the possible causes.
                You You will need to use the context provided and the agents you consider usefull to redact a message in which you explain what may cause the error message.

                Here are the available agents and their descriptions:
                    {", ".join([f"- {agent.name}: {agent.description}" for agent in self.agents])}
                Warning Messge Log:
                    {warning_messages_log}

                ###Guidelines###
                - Sometimes you might have to use multiple agent's to redact redact your message.
                - Read the warning messages provided in the context, take your time to understand, see if you could provide some possibles cause for all the warning messges.
                - If there are no actions to be taken, then make the action "respond_to_user" with your final thoughts combining all previous responses as input.
                - Respond with "respond_to_user" only when there are no agents to select from or there is no next_action
                - You will return the agent name in the form of {response_format}
            """

        self.memory = self.memory[-self.max_memory:]
        prompt = get_prompt(warning_messages_log)
        llm_response = query_llm(prompt, OrchestratorResponse)

        llm_response = ast.literal_eval(llm_response)
        print("Here the response: ",llm_response)
        print(type(llm_response))
        # #extreact the json from the llm response
        # # llm_response = jason
        # print(f"LLM Response: {llm_response}")
        #
        # action = llm_response["action"]
        # # need to define the new user input, that consider the warning_messages_log and the new informations
        #
        # print(f"Action identified by LLM: {action}")
        #
        # if action == "respond_to_user":
        #     return llm_response
        # for agent in self.agents:
        #     if agent.name == action:
        #         print("*****************Found Agent Name**************************************")
        #         agent_response = agent.process_input(user_input)
        #         print(f"{action} response: {agent_response}")
        #         self.memory.append(f"Agent Response for Task: {agent_response}")
        #         print(self.memory)
        #         return agent_response
        #

if __name__ == "__main__":
    # weather_agent = Agent(
    #     name="Weather Agent",
    #     description="Provides weather information for a given location",
    #     tools=[WeatherTool()])
    # orchestrator=AgentOrchestrator([])
    # warning_messages_log = [
    #         {"temp": 10.0, "time": "10:30", "message": "Detected temperature under the threshold"},
    #         {"temp": 10.0, "time": "10:34", "message": "Detected temperature under the threshold"},
    #         ]
    #
    # orchestrator.orchestrator_tasks(warning_messages_log)
    print("test")
