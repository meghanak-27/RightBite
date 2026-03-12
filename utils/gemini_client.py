# utils/gemini_client.py
import os
from google import genai  # switched from deprecated generativeai
import logging

API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def query_gemini(prompt: str, model: str = "models/text-bison-001", temperature: float = 0.7) -> str:
    """
    Send prompt to Gemini LLM and return generated text
    """
    try:
        response = genai.text.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            candidate_count=1,
        )
        return response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return f"[Error]: Gemini API failed: {e}"