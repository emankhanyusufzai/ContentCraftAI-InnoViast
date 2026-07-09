# utils/templates.py
# ContentCraft AI - Template Definitions
# Har content type ka icon, description, aur prompt-building logic yahan hai

TEMPLATES = {
    "Blog Post": {
        "icon": "📝",
        "description": "Long-form blog articles with intro, body, and conclusion",
        "placeholder": "e.g. Benefits of remote work for small businesses",
    },
    "Social Media Caption": {
        "icon": "📸",
        "description": "Catchy captions with hashtags for Instagram/Facebook",
        "placeholder": "e.g. New coffee shop launch in Lahore",
    },
    "Ad Copy": {
        "icon": "📢",
        "description": "Persuasive advertising copy that drives action",
        "placeholder": "e.g. Summer sale on winter jackets, 50% off",
    },
    "Email": {
        "icon": "📧",
        "description": "Professional or marketing emails",
        "placeholder": "e.g. Follow-up email after a client meeting",
    },
    "Product Description": {
        "icon": "🛍️",
        "description": "E-commerce ready product descriptions",
        "placeholder": "e.g. Wireless noise-cancelling headphones",
    },
    "LinkedIn Post": {
        "icon": "💼",
        "description": "Professional posts for career/business updates",
        "placeholder": "e.g. Announcing my new internship at a tech startup",
    },
}

TONES = ["Professional", "Casual", "Friendly", "Persuasive", "Formal"]
LENGTHS = ["Short", "Medium", "Long"]
AUDIENCES = ["General", "Business", "Students", "Marketers"]
OUTPUT_FORMATS = ["Plain Text", "Markdown"]
LANGUAGES = ["English", "Roman Urdu"]


def get_template_names():
    """Returns list of all template names for sidebar."""
    return list(TEMPLATES.keys())


def get_template_info(template_name):
    """Returns icon, description, placeholder for a given template."""
    return TEMPLATES.get(template_name, {})


def build_prompt(template_name, topic, tone, length, audience, output_format,
                  language="English", include_seo=False):
    """
    Builds the final prompt string sent to Gemini API,
    based on selected template + controls.
    """

    length_map = {
        "Short": "in about 80-120 words",
        "Medium": "in about 200-300 words",
        "Long": "in about 400-600 words",
    }

    format_instruction = (
        "Format the output using Markdown (headings, bold, bullet points where relevant)."
        if output_format == "Markdown"
        else "Provide the output as plain text without any markdown symbols."
    )

    base_instructions = {
        "Blog Post": (
            f"Write a {tone.lower()} blog post about: {topic}. "
            f"Include a catchy title, an engaging introduction, 2-3 body sections, "
            f"and a short conclusion. Write it {length_map[length]}."
        ),
        "Social Media Caption": (
            f"Write a {tone.lower()} social media caption about: {topic}. "
            f"Make it catchy and engaging, and include 3-5 relevant hashtags. "
            f"Write it {length_map[length]}."
        ),
        "Ad Copy": (
            f"Write {tone.lower()} advertising copy about: {topic}. "
            f"Focus on persuasion and a clear call-to-action. Write it {length_map[length]}."
        ),
        "Email": (
            f"Write a {tone.lower()} email about: {topic}. "
            f"Include a subject line, greeting, body, and sign-off. Write it {length_map[length]}."
        ),
        "Product Description": (
            f"Write a {tone.lower()} product description for: {topic}. "
            f"Highlight key features and benefits, and make it appealing to buyers. "
            f"Write it {length_map[length]}."
        ),
        "LinkedIn Post": (
            f"Write a {tone.lower()} LinkedIn post about: {topic}. "
            f"Make it professional yet engaging, suitable for a career/business audience. "
            f"Write it {length_map[length]}."
        ),
    }

    instruction = base_instructions.get(template_name, f"Write content about: {topic}")

    language_instruction = (
        "Write the entire content in Roman Urdu (Urdu language written using English/Latin letters)."
        if language == "Roman Urdu"
        else "Write the content in English."
    )

    seo_instruction = (
        "\nAt the very end, add a section titled 'SEO Keywords:' followed by 5-6 "
        "relevant, comma-separated SEO keywords for this content."
        if include_seo
        else ""
    )

    prompt = (
        f"{instruction}\n\n"
        f"Target audience: {audience}.\n"
        f"{language_instruction}\n"
        f"{format_instruction}"
        f"{seo_instruction}\n"
        f"Do not include any explanations or notes outside the content itself."
    )

    return prompt