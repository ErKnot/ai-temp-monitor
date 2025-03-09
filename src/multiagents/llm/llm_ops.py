from google import genai
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import BaseModel

 
def query_llm(prompt: str, reponse_format: BaseModel) -> str:
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
    config={ 
        'response_mime_type': 'application/json',
        'response_schema': reponse_format, 
            })
            
    final_response = response.text.strip()
    print(final_response)
    return final_response

if __name__ == "__main__":
    class ResponseModelTest(BaseModel):
        key1: str
        key2: str


    prompt = "can you give me a dummy response just to check that you work well?"
    print(type(query_llm(prompt, ResponseModelTest)))
