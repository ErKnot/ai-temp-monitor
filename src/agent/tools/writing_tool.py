from textwrap import dedent
import json
from src.agent.tools.base_tool import Tool
from src.agent.llm.llm_ops import query_llm
from pydantic import BaseModel

class WritingToolResponse(BaseModel):
    message: str

class WritingTool(Tool):
    def name(self):
        return "Writing Tool"

    def description(self):
        return dedent(
        """
        Analize the warnings and context and provide possible causes. 
        It take as input a string with the wornings and the context."
        """
        )       
    def use(self, prompt: str):

        prompt = dedent(f"""
        You are an AI assistant responsible of analyzing wornings and diagnosing possible causes.
        You will be provided with warnings to analyze and a context with some informations usefull for the analysis.

        ### Warnings and context ###
        {prompt}

        ### Guidelines ###
        - First write a summary of the warnings.
        - Use the context to infer some possible causes of the warnings.
        """ )

        llm_response = query_llm(prompt, WritingToolResponse)
        llm_response = json.loads(llm_response) 

        return llm_response["message"]
