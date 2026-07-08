# ContentCraft AI

**Your AI-Powered Content Writing Studio**

A Streamlit-based content generation tool that uses Google Gemini to create high-quality, structured content across six templates — blog posts, social media captions, ad copy, emails, product descriptions, and LinkedIn posts.

🔗 **Live App:** [contentcraftai-innoviast-4wzqbszlk6zxizzlsu9qsc.streamlit.app](https://contentcraftai-innoviast-4wzqbszlk6zxizzlsu9qsc.streamlit.app)

---

## 📌 Problem Statement

Creating consistent, high-quality content across different formats (blogs, social captions, ads, emails, etc.) is time-consuming and requires switching context between tone, audience, and structure for each piece. ContentCraft AI solves this by giving users a single studio where they pick a content type, customize tone/length/audience/format, and get AI-generated, ready-to-use content in seconds — fully editable and exportable.

---

## ✨ Features

- **6 Content Templates:** Blog Post, Social Media Caption, Ad Copy, Email, Product Description, LinkedIn Post
- **Customization Controls:** Tone, Length, Audience, and Output Format for every template
- **Gemini API Integration:** Real-time content generation using `gemini-2.5-flash`
- **Copy to Clipboard:** One-click copy of generated content
- **Export Options:** Download content as `.txt`, `.md` (Markdown), or `.pdf`
- **History:** Tracks the last 10 generations (template + topic) in-session
- **Error Handling:** Input validation (empty/too short/too long topics) and friendly API error messages (rate limits, network issues, safety filters)
- **Prompt Transparency:** "Prompt Strategy" panel shows mentors exactly what prompt is sent to Gemini
- **Dark / Light Theme Toggle:** Premium SaaS-style UI with a custom AI Brain + Pen Nib logo, blue-purple gradient accents

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App Framework | Streamlit |
| AI Model | Google Gemini API (`gemini-2.5-flash`) |
| Language | Python 3.14 |
| PDF Export | fpdf2 |
| Environment Management | python-dotenv |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure

```
ContentCraftAI-InnoViast/
├── assets/screenshots/       # App screenshots for documentation
├── prompts/
│   └── system_prompt.txt     # Base system prompt used for generation
├── utils/
│   ├── content_generator.py  # Gemini API connection + generation logic
│   ├── error_handler.py      # Input validation + friendly error messages
│   ├── exporters.py          # PDF export helper
│   └── templates.py          # Template definitions + prompt builder
├── .env                       # API key (not committed to GitHub)
├── .gitignore
├── AI_USAGE.md                 # AI tools/prompts used during development
├── app.py                      # Main Streamlit application
├── README.md
└── requirements.txt
```

---

## ⚙️ Setup Instructions (Run Locally)

1. **Clone the repository**
   ```bash
   git clone https://github.com/emankhanyusufzai/ContentCraftAI-InnoViast.git
   cd ContentCraftAI-InnoViast
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key**
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your browser.

---

## 🖼️ Screenshots

> _Add screenshots here from `assets/screenshots/` — e.g. gallery view, generator view, generated result with copy/download buttons._

| Gallery View | Generator View |
|---|---|
| ![Gallery](assets/screenshots/gallery.png) | ![Generator](assets/screenshots/generator.png) |

---

## 🧠 Prompt Strategy

Each template builds a structured prompt combining: content type, topic, tone, length, audience, and output format. This is visible live in the app under **"Prompt Strategy (for mentor review)"** on the generator page. Prompt iterations and reasoning are documented in [`AI_USAGE.md`](./AI_USAGE.md).

---

## 📚 Learning Outcomes

- Integrated a third-party LLM API (Google Gemini) into a Python web app end-to-end
- Learned to debug Streamlit-specific rendering quirks (HTML/Markdown code-block misinterpretation)
- Handled real-world API lifecycle issues (model deprecation, migrating from `gemini-1.5-flash` to `gemini-2.5-flash`)
- Implemented clipboard interaction via embedded JavaScript in a Python-rendered app
- Practiced clean error handling separating validation errors from API/network errors
- Deployed and managed secrets on Streamlit Community Cloud

---

## 👤 Author

Built as part of the **InnoViast Internship Program** — Track 03: AI Solutions Engineering, Week 2 Assignment.
