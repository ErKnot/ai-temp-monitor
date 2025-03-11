from google import genai
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import BaseModel


def query_llm(prompt: str, response_format: BaseModel):
    """
    Query a Large Language Model (LLM) using the Gemini API.

    This function sends a prompt to the Gemini API to generate content based on the provided prompt.

    Args:
    - prompt (str): The prompt or query to send to the LLM for content generation.
    - reponse_format (BaseModel): A Pydantic model that defines the expected response schema.

    Returns:
    - str: The generated content response from the LLM, according to the provided response format 
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
            model='gemini-2.0-pro-exp-02-05',
            contents=prompt,
    config={ 
        'response_mime_type': 'application/json',
        'response_schema': response_format, 
            })
            
    final_response = response.text.strip()
    return final_response

