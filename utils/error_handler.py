# utils/error_handler.py
# ContentCraft AI - Input Validation & Error Handling

MIN_LENGTH = 3
MAX_LENGTH = 500


def validate_input(topic: str):
    """
    Validates user's topic input before sending to Gemini API.
    Returns (is_valid: bool, error_message: str)
    """

    if topic is None or topic.strip() == "":
        return False, "⚠️ Please enter a topic before generating content."

    cleaned = topic.strip()

    if len(cleaned) < MIN_LENGTH:
        return False, f"⚠️ Topic is too short. Please enter at least {MIN_LENGTH} characters."

    if len(cleaned) > MAX_LENGTH:
        return False, f"⚠️ Topic is too long. Please keep it under {MAX_LENGTH} characters."

    # Basic check against suspicious/empty patterns
    if cleaned.count(" ") == len(cleaned):
        return False, "⚠️ Please enter valid text, not just spaces."

    return True, ""


def handle_api_error(exception: Exception) -> str:
    """
    Converts raw API/exception errors into user-friendly messages.
    """
    error_str = str(exception).lower()

    if "api key" in error_str or "authentication" in error_str or "permission" in error_str:
        return "🔑 API key error. Please check your Gemini API key in the .env file."

    if "quota" in error_str or "rate limit" in error_str or "429" in error_str:
        return "⏳ Rate limit reached. Please wait a moment and try again."

    if "timeout" in error_str or "connection" in error_str:
        return "🌐 Network issue. Please check your internet connection and try again."

    if "safety" in error_str or "blocked" in error_str:
        return "🚫 This request was blocked by content safety filters. Try rephrasing your topic."

    return "❌ Something went wrong while generating content. Please try again."
