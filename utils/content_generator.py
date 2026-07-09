# utils/content_generator.py
# ContentCraft AI - Gemini API Connection & Content Generation

import os
from google import genai
from dotenv import load_dotenv
from utils.templates import build_prompt
from utils.error_handler import handle_api_error

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

_client = None
_system_prompt = None

MODEL_NAME = "gemini-2.5-flash"


def _get_client():
    """Lazily creates and returns the Gemini client (avoids re-creating every call)."""
    global _client
    if _client is None:
        if not API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        _client = genai.Client(api_key=API_KEY)
    return _client


def _get_system_prompt():
    """Lazily reads the base system prompt from prompts/system_prompt.txt (read once, cached)."""
    global _system_prompt
    if _system_prompt is None:
        try:
            with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
                _system_prompt = f.read().strip()
        except FileNotFoundError:
            _system_prompt = ""  # falls back gracefully if the file is missing
    return _system_prompt


def generate_content(template_name, topic, tone, length, audience, output_format,
                      language="English", include_seo=False):
    """
    Main function: builds prompt, calls Gemini API, returns (success, result_or_error).
    """
    try:
        user_prompt = build_prompt(
            template_name, topic, tone, length, audience, output_format,
            language=language, include_seo=include_seo,
        )

        system_prompt = _get_system_prompt()
        full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}" if system_prompt else user_prompt

        client = _get_client()
        response = client.models.generate_content(model=MODEL_NAME, contents=full_prompt)

        if not response or not response.text:
            return False, "❌ No content was generated. Please try again with a different topic."

        return True, response.text.strip()

    except Exception as e:
        return False, handle_api_error(e)