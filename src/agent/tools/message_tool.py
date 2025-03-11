from google import genai
from google.genai import types
from src.agent.tools.base_tool import Tool
import os
from dotenv import load_dotenv
load_dotenv()

class MessageTool(Tool):
    def name(self):
        return "Message Tool"

    def description(self):
        return "Give a description of the worning message and provide some possible causes given the context provided."

    def use(self, context: list):
        api_key = os.getenv("GEMINI_API_KEY")
        
        response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=self.content,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                    )
                )
