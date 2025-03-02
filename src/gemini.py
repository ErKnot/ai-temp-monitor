import yaml
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# create the agent we will use
class AI_temp_monitor_agent():
    def __init__(self):
        load_dotenv()

        # set the gemini client
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=gemini_api_key)
        
        # set the agent configuration
        config_path = "config/agent.yaml"
        with open(config_path, "r") as file:
            agent_config = yaml.safe_load(file)
        self.content = agent_config["ai_assistant"]["content"]
        self.system_instruction = agent_config["ai_assistant"]["system_instruction"] 


    def load_warnings(self, warnings: list):
        self.content = self.content.format(warning=warnings)


    def generate_content(self):
        response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=self.content,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                    )
                )
                
        return response.text

if __name__=="__main__":
    agent = AI_temp_monitor_agent()
    warning = "This is a warning message"
    agent.load_warnings(warning)
    print(agent.content)
