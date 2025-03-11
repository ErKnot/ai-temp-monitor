from src.agent.llm.llm_ops import query_llm
from pydantic import BaseModel

class ResponseFormat(BaseModel):
    answer: str
prompt = input("You: ")
response = query_llm(prompt, response_format=ResponseFormat)
print(response)
print(type(response))
