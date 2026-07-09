# AI_USAGE.md

This document records how AI tools were used during the development of **ContentCraft AI**, as required by the InnoViast Assignment 2 guidelines.

---

## AI Tools Used

- **Claude (Anthropic)** — used for architecture planning, writing Python/Streamlit code, debugging runtime errors, and fixing UI rendering issues.
- **Google Gemini API (`gemini-2.5-flash`)** — the core AI model powering the app itself (content generation for all 6 templates).

---

## How AI Was Used

### 1. Project Scaffolding
Asked Claude to design the folder structure and initial file breakdown (`app.py`, `utils/content_generator.py`, `utils/templates.py`, `utils/error_handler.py`) based on the assignment's required scope: 6 content templates with tone/length/audience/format controls.

### 2. UI Design
Requested an **original** premium SaaS-style interface — explicitly instructed the AI *not* to copy any reference UI, but to use it only as inspiration. Specified requirements: dark theme by default with a light toggle, a custom AI Brain + Pen Nib logo (SVG, not a stock icon), and a blue-to-purple gradient as the primary accent.

### 3. Gemini API Integration
Had Claude write `content_generator.py` to connect to the Gemini API, build prompts from user inputs (topic, tone, length, audience, format), and return generated text with error handling.

### 4. Prompt Strategy Iteration
The prompt sent to Gemini is dynamically built in `templates.py` from five variables (template type, topic, tone, length, audience, format) rather than being a single static string. This was an iteration on an early version that used one fixed prompt per template — the parameterized version was chosen so tone/length/audience/format controls actually change the output instead of just the UI state.

### 5. Debugging (major iteration cycle)
- **Bug:** Custom HTML (logo, headers, cards) was rendering as visible raw text instead of formatted HTML.
  **Diagnosis (with AI help):** Streamlit's Markdown parser interprets any line indented 4+ spaces as a code block. `textwrap.dedent()` only strips *common* leading whitespace, so nested `<div>` tags still had leftover indentation that triggered this behavior.
  **Fix:** Added a `render_html()` helper that strips *all* leading whitespace from every line before rendering, used consistently across the app.

- **Bug:** Content generation failed with a generic "Something went wrong" message.
  **Diagnosis:** Traced the real exception in the terminal — Gemini's `gemini-1.5-flash` model had been fully deprecated/shut down, causing a silent 404 that the generic error handler swallowed.
  **Fix:** Updated the model to `gemini-2.5-flash`.

- **Bug:** The Copy-to-clipboard button rendered as raw HTML/JS text instead of a working button.
  **Diagnosis:** The `onclick="..."` attribute was double-quoted, and the JSON-encoded content (`json.dumps`) also starts with a double quote — the browser parsed the attribute as ending early, breaking the tag.
  **Fix:** Rewrote the component to attach the click handler via `addEventListener` inside a `<script>` tag instead of inline `onclick`, so the JSON string never collides with an HTML attribute boundary.

### 6. Deployment Support
Used Claude to walk through Git/GitHub setup, `.gitignore` configuration (excluding `.env` and `__pycache__`), and Streamlit Community Cloud deployment, including configuring `GEMINI_API_KEY` as a Cloud secret instead of relying on the local `.env` file.

### 7. Documentation
Used Claude to draft `README.md` and this `AI_USAGE.md` file, based on the actual features and fixes implemented during development.

---

## What Was Not AI-Generated
- The actual topics/content typed into the app during testing (e.g. "Benefits of Artificial Intelligence for Students") were provided by the developer, not the AI.
- Final review, testing, and verification of every fix (screenshots, manual testing of Copy/Download/History/Error handling) were performed manually by the developer before accepting any change.

---

## Reflection
AI tools significantly sped up scaffolding and debugging (especially diagnosing the Streamlit-specific HTML/Markdown rendering issue and the HTML-attribute/JSON quoting conflict in the Copy button), but every suggested fix was tested locally before being committed, and the developer verified functionality (model change, error handling, deployment) end-to-end rather than accepting code changes blindly.