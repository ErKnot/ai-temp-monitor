from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import BaseModel


def query_llm(prompt: str, response_format: BaseModel, system_instruction: str = None) -> str:
    """
    Query a Large Language Model (LLM) using the Gemini API.

    This function sends a prompt to the Gemini API to generate content based on the provided prompt and system_instruction.

    Args:
        prompt (str): The prompt to send to the LLM for content generation.
        response_format (BaseModel): A Pydantic model that defines the expected response schema.
        system_instruction (str, optional): An optional instruction to guide the LLM's response generation.

    Returns:
        str: The generated content response from the LLM, formatted according to the provided response format.
    
    Raises:
        ValueError: If the response from the Gemini API is invalid or cannot be parsed.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
    config=types.GenerateContentConfig( 
        response_mime_type='application/json',
        response_schema=response_format, 
        system_instruction=system_instruction
            )
        )
            
    final_response = response.text.strip()
    return final_response





def query_llm_original(prompt: str, response_format: BaseModel, system_instruction: str = None) -> str:
    """
    Query a Large Language Model (LLM) using the Gemini API.

    This function sends a prompt to the Gemini API to generate content based on the provided prompt and system_instruction.

    Args:
        prompt (str): The prompt to send to the LLM for content generation.
        response_format (BaseModel): A Pydantic model that defines the expected response schema.
        system_instruction (str, optional): An optional instruction to guide the LLM's response generation.

    Returns:
        str: The generated content response from the LLM, formatted according to the provided response format.
    
    Raises:
        ValueError: If the response from the Gemini API is invalid or cannot be parsed.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
    config=types.GenerateContentConfig( 
        response_mime_type='application/json',
        response_schema=response_format, 
        system_instruction=system_instruction
            )
        )
    print(response)
            
    final_response = response.text.strip()
    return final_response

