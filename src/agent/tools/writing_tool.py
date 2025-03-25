from textwrap import dedent
import json
from src.agent.tools.base_tool import Tool
from src.agent.llm.llm_ops import query_llm
from pydantic import BaseModel

class WritingToolResponse(BaseModel):
    message: str

class WritingTool(Tool):
    def name(self) -> str:
        return "Writing Tool"

    def description(self) -> str:

        return dedent(
        """
        Analize the warnings and context to provide possible causes. 
        this tool takes as input a string containing wornings and the context formatted as follow: 
        '''
        ### Warnings:
        all the warnings

        ### Context
        the context
        '''
        """
        )       
    def use(self, prompt: str) -> str:

        prompt = dedent(f"""
        You are an AI assistant responsible of analyzing wornings and diagnosing possible causes.
        You will be provided with warnings to analyze and a context with some informations useful for the analysis. The context is provided by an orchestrator and other possible tools.

        ### Warnings and context ###
        {prompt}

        ### Guidelines ###
        - First write a summary of the warnings.
        - Use the context to infer some possible causes of the warnings.
        """ )

        llm_response = query_llm(prompt, WritingToolResponse)
        llm_response = json.loads(llm_response) 

        return llm_response["message"]
