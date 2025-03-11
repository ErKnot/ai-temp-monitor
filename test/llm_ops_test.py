from src.agent.llm.llm_ops import query_llm
from pydantic import BaseModel

class ResponseFormat(BaseModel):
    entry_1: str
    entry_2: str
    entry_3: str

prompt = "Can you give me a mock response for test checking?"
response = query_llm(prompt, response_format=None)
print(response)
print(type(response))
