# utils/content_generator.py
# ContentCraft AI - Gemini API Connection & Content Generation

import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.templates import build_prompt
from utils.error_handler import handle_api_error

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

_model = None


def _get_model():
    """Lazily configures and returns the Gemini model (avoids re-configuring every call)."""
    global _model
    if _model is None:
        if not API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        genai.configure(api_key=API_KEY)
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model


def generate_content(template_name, topic, tone, length, audience, output_format):
    """
    Main function: builds prompt, calls Gemini API, returns (success, result_or_error).
    """
    try:
        prompt = build_prompt(template_name, topic, tone, length, audience, output_format)

        model = _get_model()
        response = model.generate_content(prompt)

        if not response or not response.text:
            return False, "❌ No content was generated. Please try again with a different topic."

        return True, response.text.strip()

    except Exception as e:
        return False, handle_api_error(e)
